#include <cstdint>
#include <exception>
#include <format>
#include <iostream>
#include <string>
#include <vector>

#define DEBUG 1

#ifdef DEBUG
    #define LOG_DEBUG(...) printf(__VA_ARGS__);
#elif
    #define LOG_DEBUG(...)
#endif

#ifdef _WIN32
    #include <windows.h>

struct FileMapping {
    HANDLE        hFile;
    HANDLE        hMapFile;
    LPVOID        lpBase;
    LARGE_INTEGER size;
    bool          is_ok = false;

    FileMapping(const char* filename) {
        hFile = CreateFile(
            filename,
            GENERIC_READ,
            FILE_SHARE_READ,
            NULL,
            OPEN_EXISTING,
            FILE_ATTRIBUTE_NORMAL,
            NULL
        );

        if (hFile == INVALID_HANDLE_VALUE) {
            std::cerr << "Could not open file." << std::endl;
            return;
        }

        if (!GetFileSizeEx(hFile, &size)) {
            std::cerr << "Could not get file size." << std::endl;
            CloseHandle(hFile);
            return;
        }

        hMapFile = CreateFileMapping(hFile, NULL, PAGE_READONLY, 0, 0, NULL);

        if (hMapFile == NULL) {
            std::cerr << "Could not create file mapping object." << std::endl;
            CloseHandle(hFile);
            return;
        }

        lpBase = MapViewOfFile(hMapFile, FILE_MAP_READ, 0, 0, 0);

        if (lpBase == NULL) {
            std::cerr << "Could not map view of file." << std::endl;
            CloseHandle(hMapFile);
            CloseHandle(hFile);
            return;
        }

        is_ok = true;
    }

    ~FileMapping() {
        UnmapViewOfFile(this->lpBase);
        CloseHandle(this->hMapFile);
        CloseHandle(this->hFile);
    }

    void* GetMapping() {
        return lpBase;
    }

    uint64_t GetSize() {
        return this->size.QuadPart;
    }
};

#elif __unix__

    #include <fcntl.h>
    #include <sys/mman.h>
    #include <sys/stat.h>
    #include <unistd.h>

class FileMapping {
    int    fd;
    void*  map;
    size_t size;
    bool   is_ok = false;

    FileMapping(const char* filename) {
        fd = open(filename, O_RDONLY);
        if (fd == -1) {
            std::cerr << "Could not open file." << std::endl;
            return;
        }

        struct stat st;
        if (fstat(fd, &st) == -1) {
            std::cerr << "Could not get file size." << std::endl;
            close(fd);
            return;
        }

        size = st.st_size;
        map  = mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);

        if (map == MAP_FAILED) {
            std::cerr << "Could not map file." << std::endl;
            close(fd);
            return;
        }

        is_ok = true;
    }

    ~FileMapping() {
        munmap(map, size);
        close(fd);
    }

    void* GetMapping() {
        return lpBase;
    }

    uint64_t GetSize() {
        return this->size;
    }
}

#endif

enum class TokenType {
    UNKNOWN         = 0,
    INVALID         = 1,
    INTEGER         = 2,
    SIGN            = 3,
    G01_CODE        = 4,
    G02_CODE        = 5,
    G03_CODE        = 6,
    G04_CODE        = 7,
    G36_CODE        = 8,
    G37_CODE        = 9,
    G54_CODE        = 10,
    G55_CODE        = 11,
    G70_CODE        = 12,
    G71_CODE        = 13,
    G74_CODE        = 14,
    G75_CODE        = 15,
    G90_CODE        = 16,
    G91_CODE        = 17,
    D01_CODE        = 18,
    D02_CODE        = 19,
    D03_CODE        = 20,
    DNN_SELECT      = 21,
    STRING          = 22,
    COORDINATE_CODE = 23,
    END_COMMAND,
    STATEMENT_BOUNDARY,
};

struct Token {
    std::string    content;
    enum TokenType type;
};

struct CommandToken : Token {};

struct ExtendedCommand : Token {};

struct GerberTokenizer {

    class EndOfFile : std::exception {};

    class InvalidToken : std::exception {

        std::string message;
        uint64_t    failure_char_index;

      public:
        InvalidToken(uint64_t failure_char_index, std::string message) :
            failure_char_index(failure_char_index),
            message(message) {}

        const char* what() const noexcept override {
            return message.c_str();
        }
    };

    enum class Result {
        CONSUMED,
        ABORTED,
    };

    char*              gerber_code;
    uint64_t           gerber_code_size;
    std::vector<Token> tokens_vector;

    GerberTokenizer(char* file_mapping, uint64_t file_size) :
        gerber_code(file_mapping),
        gerber_code_size(file_size) {}

    bool tokenize() {
        uint64_t current_char_index = 0;
        try {
            while (current_char_index < gerber_code_size) {
                current_char_index = tokenize_next(current_char_index);
            }
        } catch (GerberTokenizer::EndOfFile) {
            return true;
        }
        return true;
    }

    std::string make_substring(uint64_t begin_token_index, uint64_t current_char_index) {
        return std::string(gerber_code + begin_token_index, gerber_code + current_char_index);
    }

    void make_token(uint64_t begin_token_index, uint64_t current_char_index, enum TokenType type) {
        tokens_vector.push_back({make_substring(begin_token_index, current_char_index), type});

        std::cout << tokens_vector.back().content << " " << int(tokens_vector.back().type)
                  << std::endl;
    }

    [[noreturn]] void throw_invalid_token(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            if (begin_token_index > 0) {
                begin_token_index--;
            }
            if (current_char_index > 0) {
                current_char_index--;
            }
        }
        std::string message = std::format(
            "Invalid token '{}' at index: {}",
            make_substring(begin_token_index, current_char_index + 1),
            begin_token_index
        );
        throw InvalidToken(begin_token_index, message);
    }

    uint64_t tokenize_next(uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            throw EndOfFile();
        }
        char current_char = gerber_code[current_char_index];

        switch (current_char) {
            case '*':
                return tokenize_asterisk(current_char_index, current_char_index);
            case 'G':
                return tokenize_g_code(current_char_index, current_char_index + 1);
            case 'D':
                return tokenize_d_code(current_char_index, current_char_index + 1);
            case 'X':
            case 'Y':
            case 'I':
            case 'J':
                make_token(current_char_index, current_char_index + 1, TokenType::COORDINATE_CODE);
                return tokenize_signed_integer(current_char_index + 1, current_char_index + 1);
            case ' ':
            case '\t':
            case '\n':
            case '\r':
                return current_char_index + 1;
            default:
                throw_invalid_token(current_char_index, current_char_index + 1);
        }
        throw_invalid_token(current_char_index, current_char_index + 1);
    }

    uint64_t tokenize_asterisk(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '*':
                make_token(begin_token_index, current_char_index + 1, TokenType::END_COMMAND);
                return current_char_index + 1;
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_string(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            make_token(begin_token_index, current_char_index, TokenType::STRING);
            return current_char_index - 1;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '*':
            case '%':
                make_token(begin_token_index, current_char_index, TokenType::STRING);
                return current_char_index - 1;
            default:
                return tokenize_string(begin_token_index, current_char_index + 1);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_g_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
                return tokenize_g_code(begin_token_index, current_char_index + 1);
            case '1':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G01_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '2':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G02_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '3':
                if (is_a_number(current_char_index + 1)) {
                    return tokenize_g3_code(begin_token_index, current_char_index + 1);
                } else {
                    make_token(begin_token_index, current_char_index + 1, TokenType::G03_CODE);
                    return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
                }
            case '4':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G04_CODE);
                if (!is_asterisk(current_char_index + 1)) {
                    current_char_index =
                        tokenize_string(current_char_index + 1, current_char_index + 1);
                }
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '5':
                if (is_a_number(current_char_index + 1)) {
                    return tokenize_g5_code(begin_token_index, current_char_index + 1);
                }
                throw_invalid_token(begin_token_index, current_char_index + 1);
            case '7':
                if (is_a_number(current_char_index + 1)) {
                    return tokenize_g7_code(begin_token_index, current_char_index + 1);
                }
                throw_invalid_token(begin_token_index, current_char_index + 1);
            case '9':
                if (is_a_number(current_char_index + 1)) {
                    return tokenize_g9_code(begin_token_index, current_char_index + 1);
                }
                throw_invalid_token(begin_token_index, current_char_index + 1);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_g3_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '6':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G36_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '7':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G37_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_g5_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '4':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G54_CODE);
                // tokenize D code.
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '5':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G55_CODE);
                // tokenize D03 code.
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_g7_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G70_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '1':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G71_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '4':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G74_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '5':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G75_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_g9_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G90_CODE);
                // tokenize D code.
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '1':
                if (is_a_number(current_char_index + 1))
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::G91_CODE);
                // tokenize D03 code.
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_d_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
                return tokenize_d_code(begin_token_index, current_char_index + 1);
            case '1':
                if (is_a_number(current_char_index + 1))
                    return tokenize_d_select(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::D01_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '2':
                if (is_a_number(current_char_index + 1))
                    return tokenize_d_select(begin_token_index, current_char_index + 1);
                make_token(begin_token_index, current_char_index + 1, TokenType::D02_CODE);
                return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
            case '3':
                if (is_a_number(current_char_index + 1)) {
                    return tokenize_d_select(begin_token_index, current_char_index + 1);
                } else {
                    make_token(begin_token_index, current_char_index + 1, TokenType::D03_CODE);
                    return tokenize_asterisk(current_char_index + 1, current_char_index + 1);
                }
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                return tokenize_d_select(begin_token_index, current_char_index + 1);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_d_select(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                return tokenize_d_select(begin_token_index, current_char_index + 1);
            default:
                make_token(begin_token_index, current_char_index, TokenType::DNN_SELECT);
                return tokenize_asterisk(current_char_index, current_char_index);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_signed_integer(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            if (begin_token_index == current_char_index) {
                throw_invalid_token(begin_token_index, current_char_index + 1);
            }
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '-':
            case '+':
                return tokenize_unsigned_integer(begin_token_index, current_char_index + 1);
            default:
                return tokenize_unsigned_integer(begin_token_index, current_char_index);
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    uint64_t tokenize_unsigned_integer(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            if (begin_token_index == current_char_index) {
                throw_invalid_token(begin_token_index, current_char_index + 1);
            }
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                return tokenize_signed_integer(begin_token_index, current_char_index + 1);
            default:
                if (begin_token_index == current_char_index) {
                    throw_invalid_token(begin_token_index, current_char_index + 1);
                }
                make_token(begin_token_index, current_char_index, TokenType::INTEGER);
                return current_char_index;
        }
        throw_invalid_token(begin_token_index, current_char_index + 1);
    }

    bool is_a_number(uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return false;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                return true;
        }
        return false;
    }

    bool is_asterisk(uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return false;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '*':
                return true;
        }
        return false;
    }
};

int main() {

    std::vector<std::string> paths = {
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G01.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G02.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G03.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G04.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G04_text.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G36.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G37.grb",
        //"C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G54.grb",
        //"C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G55.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G70.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G71.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G74.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G75.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G90.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G91.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\d_select\\D11.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\d_select\\D12.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\d_select\\D301.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\d_select\\D999.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\d_codes\\D01.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\d_codes\\D02.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\d_codes\\D03.grb",
    };
    for (auto path : paths) {
        auto  mapping_handler = FileMapping(path.c_str());
        char* mapping         = (char*)(mapping_handler.GetMapping());

        auto size = mapping_handler.GetSize();
        std::cout << path << std::endl;
        GerberTokenizer tokenizer(mapping, size);
        tokenizer.tokenize();
        // for (auto token : tokenizer.tokenized_tokens_vector) {
        //     std::cout << token.content << " " << int(token.type) << std::endl;
        // }
    }

    return 0;
}
