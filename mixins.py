class FlexibleMixin:

    def make_flexible(self, n_rows, n_cols):
        for row in range(n_rows):
            self.grid_columnconfigure(row, weight=1)

        for col in range(n_cols):
            self.grid_columnconfigure(col, weight=1)
