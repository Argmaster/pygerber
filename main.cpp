#include <array>
#include <cstdint>
#include <exception>
#include <iostream>
#include <optional>
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
    G_CODE,
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

    class EndOfMapping : std::exception {};

    class InvalidToken : std::exception {};

    enum class Result {
        CONSUMED,
        ABORTED,
    };

    char*    gerber_code;
    uint64_t gerber_code_size;
    uint64_t char_pointer = 0;

    enum TokenType     token_type = TokenType::UNKNOWN;
    std::vector<Token> parsed_tokens_vector;
    std::vector<char>   buffer;

    GerberParser(char* file_mapping, uint64_t file_size) :
        gerber_code(file_mapping),
        gerber_code_size(file_size),
        buffer(16384) {}

    bool has_next_char() {
        return char_pointer < gerber_code_size;
    }

    char get_next_char_throw() {
        std::optional<char> current = get_next_char();
        if (!current.has_value()) {
            throw EndOfMapping();
        }
        return current.value();
    }

    std::optional<char> get_next_char() {
        if (!has_next_char()) {
            return std::nullopt;
        }
        char next = gerber_code[char_pointer];
        char_pointer++;
        LOG_DEBUG("get_next_char(): %c \n", next);
        return next;
    }

    std::optional<char> get_prev_char() {
        if (char_pointer <= 0) {
            return std::nullopt;
        }
        char_pointer--;
        char next = gerber_code[char_pointer];
        return next;
    }

    bool parse() {
        while (char_pointer < gerber_code_size) {
            LOG_DEBUG("char_pointer: %llu  file_size: %llu \n", char_pointer, gerber_code_size);
            try {
                parse_next();
            } catch (GerberParser::EndOfMapping) {
                return true;
            } catch (GerberParser::InvalidToken) {
                return false;
            }
        }
        return true;
    }

    void parse_next() {
        char current = get_next_char_throw();
        switch (current) {
            case '*':
                LOG_DEBUG("Found * character. \n");
                parsed_tokens_vector.push_back(
                    {std::string(1, current), TokenType::END_COMMAND}
                );
                break;
            case 'G':
                LOG_DEBUG("Found G character. \n");
                parsed_tokens_vector.push_back({std::string(1, current), TokenType::G_CODE}
                );
                break;
            case 'X':
            case 'Y':
            case 'I':
            case 'J':
                LOG_DEBUG("Found X|Y character. \n");
                parsed_tokens_vector.push_back(
                    {std::string(1, current), TokenType::COORDINATE_CODE}
                );
                break;
            case '%':
                LOG_DEBUG("Found %% character. \n");
                parsed_tokens_vector.push_back(
                    {std::string(1, current), TokenType::STATEMENT_BOUNDARY}
                );
                break;
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
                parse_integer(current);
                break;
            case '-':
            case '+':
                parsed_tokens_vector.push_back({std::string(1, current), TokenType::SIGN});
                break;
            case ' ':
            case '\t':
            case '\n':
            case '\r':
                break;
        }
    }

    void parse_integer(char current) {
        LOG_DEBUG("Found %c character. \n", current);
        buffer.push_back(current);
        parse_integer_tail();

        LOG_DEBUG("parsed_tokens_vector %llu \n", parsed_tokens_vector.size());
        parsed_tokens_vector.push_back(
            {std::string{buffer.begin(), buffer.end()}, TokenType::INTEGER}
        );
        buffer.clear();
    }

    void parse_integer_tail() {
        while (has_next_char()) {
            std::optional<char> current = get_next_char();
            if (!current.has_value()) {
                return;
            }
            if (parse_number(current.value()) == Result::CONSUMED) {
                buffer.push_back(current.value());
                continue;
            }
            // Don't consume not matching character.
            get_prev_char();
            break;
        }
    }

    Result parse_number(char current) {
        switch (current) {
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
                LOG_DEBUG("Found %c character. \n", current);
                return Result::CONSUMED;
                break;
        }
        return Result::ABORTED;
    }
};

int main() {
    auto mapping_handler =
        FileMapping("C:\\Users\\argma\\dev\\pygerber\\test\\assets\\gerberx3\\tokens\\g_"
                    "codes\\G01.grb");
    char* mapping = (char*)(mapping_handler.GetMapping());

    auto         size = mapping_handler.GetSize();
    GerberParser parser(mapping, size);
    parser.parse();

    for (auto token : parser.parsed_tokens_vector) {
        std::cout << token.content << " " << int(token.type) << std::endl;
    }

    return 0;
}
