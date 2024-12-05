#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define FILENAME "input.txt"

typedef struct s_page_order {
  int page;
  int order[100];
} t_page_order;

int is_page_order_line(char *line) {
  int len = strlen(line);

  for (int i = 0; i < len; i++) {
    if (line[i] == '|') {
      return 1;
    }
  }
  return 0;
}

int get_page_before(char *line) {
  int n = 0;
  int i = 0;

  while (line[i] && line[i] != '|') {
    if (line[i] >= '0' && line[i] <= '9') {
      n = n * 10 + (line[i] - '0');
    }
    i++;
  }
  return n;
}

int get_page_after(char *line) {
  int n = 0;
  int i = 0;
  int found = 0;

  while (line[i]) {
    if (found) {
      if (line[i] >= '0' && line[i] <= '9') {
        n = n * 10 + (line[i] - '0');
      }
    }
    if (line[i] == '|') {
      found = 1;
    }
    i++;
  }
  return n;
}

void debug_page_orders(int **arr) {
  for (int i = 0; i < 1000; i++) {
    if (arr[i][0] != -1) {
      printf("page %d => ", i);
      for (int j = 0; j < 1000 && arr[i][j] != -1; j++) {
        printf("%d,", arr[i][j]);
      }
      printf("\n");
    }
  }
}

int count_pages(char *line) {
  int n = 0;
  int i = 0;

  while (line[i]) {
    if (line[i] == ',' || line[i] == '\n') {
      n++;
    }
    i++;
  }
  return n;
}

int *get_update_seq(char *s) {
  int *seq = malloc(1000 * sizeof(*seq));
  int i = 0;
  int j = 0;
  int n = 0;

  memset(seq, -1, 1000 * sizeof(*seq));
  while (s[i]) {
    if (s[i] >= '0' && s[i] <= '9') {
      n = n * 10 + (s[i] - '0');
    } else if (s[i] == ',' || s[i] == '\n') {
      seq[j] = n;
      n = 0;
      j++;
    }
    i++;
  }
  return seq;
}

int is_valid(int *update, int **page_orders) {
  for (int i = 1; i < 1000 && update[i] != -1; i++) {
    int p_before = update[i - 1];

    int found = 0;
    for (int j = 0; j < 1000 && page_orders[p_before][j] != -1; j++) {
      if (page_orders[p_before][j] == update[i]) {
        found = 1;
        break;
      }
    }
    if (!found) {
      return 0;
    }
  }
  return 1;
}

void moveBefore(int *arr, int idxToMove, int targetIdx) {
  int *new = malloc(1000 * sizeof(*new));
  memset(new, -1, 1000 * sizeof(*new));
  int j = 0;
  for (int i = 0; i < 1000 && arr[i] != -1; i++) {
    if (j == targetIdx) {
      j++;
    }
    if (i == idxToMove) {
      i++;
    }
    new[j] = arr[i];
    j++;
  }
  new[targetIdx] = arr[idxToMove];
  memcpy(arr, new, 1000 * sizeof(*new));
}

int *generate_new_seq(int *seq, int **page_orders) {
  for (int i = 0; i < 1000 && seq[i] != -1; i++) {
    int *p_order = page_orders[seq[i]];
    for (int j = 0; j < 1000 && seq[j] != -1; j++) {
      if (i == j) {
        continue;
      }

      for (int k = 0; k < 1000 && p_order[k] != -1; k++) {
        if (p_order[k] == seq[j]) {
          int is_before = i < j ? 1 : 0;
          if (!is_before) {
            moveBefore(seq, i, j);
            return seq;
          }
          break;
        }
      }
    }
  }
  return seq;
}

int main() {
  int **page_orders;

  page_orders = malloc(1000 * sizeof(*page_orders));
  for (int i = 0; i < 1000; i++) {
    page_orders[i] = malloc(1000 * sizeof(*page_orders[i]));
    for (int j = 0; j < 1000; j++) {
      page_orders[i][j] = -1;
    }
  }

  FILE *file = fopen(FILENAME, "r");
  int result = 0;

  if (file) {
    char line[4096];
    while (fgets(line, sizeof(line), file)) {
      if (line[0] == '\n') {
        continue;
      } else if (is_page_order_line(line)) {
        int p1 = get_page_before(line);
        int p2 = get_page_after(line);
        for (int i = 0; i < 1000; i++) {
          if (page_orders[p1][i] == -1) {
            page_orders[p1][i] = p2;
            break;
          }
        }
      } else {
        int nb_pages = count_pages(line);
        int *update_seq = get_update_seq(line);

        int valid = is_valid(update_seq, page_orders);
        if (!valid) {
          int *new_seq;
          while (!valid) {
            new_seq = generate_new_seq(update_seq, page_orders);
            valid = is_valid(new_seq, page_orders);
          }
          result += new_seq[nb_pages / 2];
        }
      }
    }
  }
  fclose(file);

  printf("%d\n", result);

  return 0;
}