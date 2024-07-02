#include <cstdint>
#include <exception>
#include <format>
#include <iostream>
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
    UNKNOWN,
    INVALID,
    INTEGER,
    SIGN,
    G01_CODE,
    G02_CODE,
    G03_CODE,
    G04_CODE,
    G36_CODE,
    G37_CODE,
    STRING,
    COORDINATE_CODE,
    D_CODE,
    END_COMMAND,
    STATEMENT_BOUNDARY,
};

struct Token {
    std::string    content;
    enum TokenType type;
};

struct CommandToken : Token {};

struct ExtendedCommand : Token {};

struct GerberParser {

    class EndOfFile : std::exception {};

    class InvalidToken : std::exception {

        std::string message;
        uint64_t    failure_char_index;

      public:
        InvalidToken(uint64_t failure_char_index) :
            failure_char_index(failure_char_index) {
            message = std::format("Invalid token at index: {}", failure_char_index);
        }

        const char* what() const noexcept override {
            return message.c_str();
        }
    };

    enum class Result {
        CONSUMED,
        ABORTED,
    };

    char*    gerber_code;
    uint64_t gerber_code_size;

    std::vector<Token> parsed_tokens_vector;
    std::vector<char>  token_buffer;

    GerberParser(char* file_mapping, uint64_t file_size) :
        gerber_code(file_mapping),
        gerber_code_size(file_size),
        token_buffer(16384) {}

    bool parse() {
        uint64_t current_char_index = 0;
        try {
            while (current_char_index < gerber_code_size) {
                current_char_index = parse_next(current_char_index);
            }
        } catch (GerberParser::EndOfFile) {
            return true;
        }
        return true;
    }

    std::string make_substring(uint64_t begin_token_index, uint64_t current_char_index) {
        return std::string(gerber_code + begin_token_index, gerber_code + current_char_index);
    }

    void make_token(uint64_t begin_token_index, uint64_t current_char_index, enum TokenType type) {
        parsed_tokens_vector.push_back({make_substring(begin_token_index, current_char_index), type}
        );
    }

    uint64_t parse_next(uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            throw EndOfFile();
        }
        char current_char = gerber_code[current_char_index];

        switch (current_char) {
            case '*':
                return parse_asterisk(current_char_index, current_char_index);
            case 'G':
                return parse_g_code(current_char_index, current_char_index + 1);
            case ' ':
            case '\t':
            case '\n':
            case '\r':
                return current_char_index + 1;
            default:
                throw InvalidToken(current_char_index);
        }
        return current_char_index + 1;
    }

    uint64_t parse_asterisk(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '*':
                make_token(begin_token_index, current_char_index + 1, TokenType::END_COMMAND);
                return current_char_index + 1;
        }
        throw InvalidToken(current_char_index);
    }

    uint64_t parse_string(uint64_t begin_token_index, uint64_t current_char_index) {
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
                return parse_string(begin_token_index, current_char_index + 1);
        }
        throw InvalidToken(current_char_index);
    }

    uint64_t parse_g_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '0':
                return parse_g_code(begin_token_index, current_char_index + 1);
            case '1':
                if (is_a_number(current_char_index + 1))
                    return begin_token_index;
                make_token(begin_token_index, current_char_index + 1, TokenType::G01_CODE);
                return parse_asterisk(current_char_index + 1, current_char_index + 1);
            case '2':
                if (is_a_number(current_char_index + 1))
                    return begin_token_index;
                make_token(begin_token_index, current_char_index + 1, TokenType::G02_CODE);
                return parse_asterisk(current_char_index + 1, current_char_index + 1);
            case '3':
                if (is_a_number(current_char_index + 1)) {
                    return parse_g3_code(begin_token_index, current_char_index + 1);
                } else {
                    make_token(begin_token_index, current_char_index + 1, TokenType::G03_CODE);
                    return parse_asterisk(current_char_index + 1, current_char_index + 1);
                }
            case '4':
                if (is_a_number(current_char_index + 1))
                    return begin_token_index;
                make_token(begin_token_index, current_char_index + 1, TokenType::G04_CODE);
                if (!is_asterisk(current_char_index + 1)) {
                    current_char_index =
                        parse_string(current_char_index + 1, current_char_index + 1);
                }
                return parse_asterisk(current_char_index + 1, current_char_index + 1);
        }
        throw InvalidToken(current_char_index);
    }

    uint64_t parse_g3_code(uint64_t begin_token_index, uint64_t current_char_index) {
        if (current_char_index >= gerber_code_size) {
            return begin_token_index;
        }
        char current_char = gerber_code[current_char_index];
        switch (current_char) {
            case '6':
                if (is_a_number(current_char_index + 1))
                    return begin_token_index;
                make_token(begin_token_index, current_char_index + 1, TokenType::G36_CODE);
                return parse_asterisk(current_char_index + 1, current_char_index + 1);
            case '7':
                if (is_a_number(current_char_index + 1))
                    return begin_token_index;
                make_token(begin_token_index, current_char_index + 1, TokenType::G37_CODE);
                return parse_asterisk(current_char_index + 1, current_char_index + 1);
        }
        throw InvalidToken(current_char_index);
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
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G70.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G71.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G73.grb",
        "C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_codes\\G74.grb",
    };
    for (auto path : paths) {
        auto  mapping_handler = FileMapping(path.c_str());
        char* mapping         = (char*)(mapping_handler.GetMapping());

        auto         size = mapping_handler.GetSize();
        GerberParser parser(mapping, size);
        parser.parse();
        std::cout << path << std::endl;
        for (auto token : parser.parsed_tokens_vector) {
            std::cout << token.content << " " << int(token.type) << std::endl;
        }
    }

    return 0;
}
