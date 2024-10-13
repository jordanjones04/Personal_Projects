#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>


#define BUFFER_SIZE 4096
#define DEFAULT_PORT 8080


void handle_client(int client_socket, const char *document_root);
void respond_with_file(int client_socket, const char *path);
void respond_with_directory_listing(int client_socket, const char *path);
void respond_with_404(int client_socket);

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <port> <document_root>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int port = atoi(argv[1]);
    const char *document_root = argv[2];

    // Change to document root directory
    if (chdir(document_root) != 0) {
        perror("chdir");
        exit(EXIT_FAILURE);
    }

    int server_socket, client_socket;
    struct sockaddr_in server_addr, client_addr;
    socklen_t client_len = sizeof(client_addr);

    // Create socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("socket");
        exit(EXIT_FAILURE);
    }

    // Bind socket to port
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(server_socket, (struct sockaddr *) &server_addr, sizeof(server_addr)) < 0) {
        perror("bind");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    listen(server_socket, 5);

    // Main loop to accept and handle clients
    while (1) {
        client_socket = accept(server_socket, (struct sockaddr *) &client_addr, &client_len);
        if (client_socket < 0) {
            perror("accept");
            continue;
        }

        handle_client(client_socket, document_root);
        close(client_socket);
    }

    close(server_socket);
    return 0;
}

void handle_client(int client_socket, const char *document_root) {
    char buffer[BUFFER_SIZE];
    int bytes_read, total_read = 0;

    // Read request from client in a loop
    while ((bytes_read = read(client_socket, buffer + total_read, BUFFER_SIZE - total_read - 1)) > 0) {
        total_read += bytes_read;
        buffer[total_read] = '\0';
        if (strstr(buffer, "\r\n\r\n")) {
            break; // Stop reading when full request received
        }
    }

    if (bytes_read < 0) {
        perror("read");
        return;
    }

    // Parse request (only GET requests)
    char method[16], path[256], protocol[16];
    sscanf(buffer, "%s %s %s", method, path, protocol);

    // Handle only GET requests for simplicity
    if (strcmp(method, "GET") != 0) {
        respond_with_404(client_socket);
        return;
    }

    // Construct full path
    char full_path[512];
    snprintf(full_path, sizeof(full_path), "%s%s", document_root, path);

    // Check if the path exists and is a file or directory
    struct stat file_stat;
    if (stat(full_path, &file_stat) < 0) {
        respond_with_404(client_socket);
        return;
    }

    if (S_ISREG(file_stat.st_mode)) {
        respond_with_file(client_socket, full_path);
    } else if (S_ISDIR(file_stat.st_mode)) {
        // Check for index.html in directory
        char index_path[512];
        snprintf(index_path, sizeof(index_path), "%s/index.html", full_path);
        if (stat(index_path, &file_stat) == 0 && S_ISREG(file_stat.st_mode)) {
            respond_with_file(client_socket, index_path);
        } else {
            respond_with_directory_listing(client_socket, full_path);
        }
    } else {
        respond_with_404(client_socket);
    }
    close(client_socket);
}


void respond_with_file(int client_socket, const char *path) {
    FILE *file = fopen(path, "rb");
    if (!file) {
        respond_with_404(client_socket);
        return;
    }

    // Determine the content type based on file extension
    const char *content_type = "application/octet-stream"; // Default content type
    const char *extension = strrchr(path, '.'); // Find the last dot in the path
    if (extension) {
        if (strcmp(extension, ".html") == 0) {
            content_type = "text/html";
        } else if (strcmp(extension, ".txt") == 0) {
            content_type = "text/plain";
        } else if (strcmp(extension, ".jpeg") == 0 || strcmp(extension, ".jpg") == 0) {
            content_type = "image/jpeg";
        } else if (strcmp(extension, ".gif") == 0) {
            content_type = "image/gif";
        } else if (strcmp(extension, ".png") == 0) {
            content_type = "image/png";
        } else if (strcmp(extension, ".pdf") == 0) {
            content_type = "application/pdf";
        } else if (strcmp(extension, ".ico") == 0) {
            content_type = "image/x-icon";
        }
    }

    // Send HTTP response headers
    dprintf(client_socket, "HTTP/1.1 200 OK\r\n");
    dprintf(client_socket, "Content-Type: %s\r\n", content_type);
    dprintf(client_socket, "Connection: close\r\n\r\n");
    printf("HTTP/1.1 200 OK\r\nContent-Type: %s\r\nConnection: close\r\n\r\n", content_type);

    // Flush the output after headers
    fsync(client_socket);

    // Send file content using send()
    char buffer[BUFFER_SIZE];
    size_t bytes_read;
    while ((bytes_read = fread(buffer, 1, BUFFER_SIZE, file)) > 0) {
        send(client_socket, buffer, bytes_read, 0);  // Use send() instead of write()
    }

    fclose(file);
}




void respond_with_directory_listing(int client_socket, const char *path) {
    dprintf(client_socket, "HTTP/1.1 200 OK\r\n");
    dprintf(client_socket, "Content-Type: text/html\r\n");
    dprintf(client_socket, "Connection: close\r\n\r\n");

    dprintf(client_socket, "<html>\n");
    dprintf(client_socket, "Directory listing for: %s<br/>\n", path);
    dprintf(client_socket, "<ul>\n");

    // Open the directory
    DIR *dir = opendir(path);
    if (dir) {
        struct dirent *entry;
        // Read entries from the directory
        while ((entry = readdir(dir)) != NULL) {
            // Ignore the current (.) and parent (..) directories
            if (strcmp(entry->d_name, ".") != 0 && strcmp(entry->d_name, "..") != 0) {
                // Check if the entry is a directory
                char full_path[512];
                snprintf(full_path, sizeof(full_path), "%s/%s", path, entry->d_name);
                struct stat file_stat;
                if (stat(full_path, &file_stat) == 0) {
                    if (S_ISDIR(file_stat.st_mode)) {
                        dprintf(client_socket, "<li><a href=\"%s/\">%s</a></li>\n", full_path, entry->d_name);
                    } else {
                        dprintf(client_socket, "<li><a href=\"%s\">%s</a></li>\n", full_path, entry->d_name);
                    }
                }
            }
        }
        closedir(dir);
    } else {
        // If opening the directory fails, handle the error appropriately
        dprintf(client_socket, "<li>Error reading directory: %s</li>\n", strerror(errno));
    }

    dprintf(client_socket, "</ul>\n");
    dprintf(client_socket, "</html>\n");
}

void respond_with_404(int client_socket) {
    dprintf(client_socket, "HTTP/1.1 404 Not Found\r\n");
    dprintf(client_socket, "Content-Type: text/html\r\n");
    dprintf(client_socket, "Connection: close\r\n\r\n");
    dprintf(client_socket, "<html><body><h1>404 Not Found</h1></body></html>");
    printf("HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n");

}
