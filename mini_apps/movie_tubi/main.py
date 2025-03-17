import sys
import csv
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QAction, QComboBox, QFileDialog, QCompleter
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

# --- Subclass QTableWidget untuk mendukung klik link ---
class ClickableTableWidget(QTableWidget):
    def mouseDoubleClickEvent(self, event):
        item = self.itemAt(event.pos())
        if item:
            text = item.text().strip()
            if text.startswith("http://") or text.startswith("https://"):
                QDesktopServices.openUrl(QUrl(text))
        super().mouseDoubleClickEvent(event)

# --- Fungsi untuk memuat data CSV ---
def load_csv_data_from_file():
    csv_path, _ = QFileDialog.getOpenFileName(
        None, "Pilih CSV File", "", "CSV Files (*.csv)"
    )
    if not csv_path:
        QMessageBox.critical(None, "Error", "File CSV belum dipilih. Aplikasi akan keluar.")
        sys.exit(1)
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            data = list(reader)
            return data
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Gagal membaca CSV:\n{str(e)}")
        sys.exit(1)

# --- Halaman HOME: Menampilkan data film lengkap dengan fitur sorting ---
class HomePage(QWidget):
    def __init__(self, movies):
        super().__init__()
        self.movies = movies
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        titleLabel = QLabel("Daftar Film")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titleLabel)
        
        self.table = ClickableTableWidget()
        self.table.setSortingEnabled(True) 
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.populate_table(self.movies)
        
    def populate_table(self, movies):
        if not movies:
            self.table.setRowCount(0)
            return
        headers = list(movies[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(movies))
        self.table.setHorizontalHeaderLabels(headers)
        for row_index, movie in enumerate(movies):
            for col_index, header in enumerate(headers):
                value = movie.get(header, "")
                item = QTableWidgetItem(value)
                self.table.setItem(row_index, col_index, item)
        self.table.resizeColumnsToContents()

# --- Halaman CARI: Pencarian dengan opsi dropdown dan auto-suggest ---
class SearchPage(QWidget):
    def __init__(self, movies):
        super().__init__()
        self.movies = movies
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        titleLabel = QLabel("Cari Film")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titleLabel)
        
        searchLayout = QHBoxLayout()
        
        self.fieldComboBox = QComboBox()
        if self.movies:
            headers = list(self.movies[0].keys())
            self.fieldComboBox.addItems(headers)
        else:
            self.fieldComboBox.addItem("title")
        searchLayout.addWidget(self.fieldComboBox)
        
        self.searchEdit = QLineEdit()
        self.searchEdit.setPlaceholderText("Masukkan kata kunci pencarian...")
        searchLayout.addWidget(self.searchEdit)
        self.updateCompleter() 
        
        self.fieldComboBox.currentIndexChanged.connect(self.updateCompleter)
        
        searchButton = QPushButton("Cari")
        searchButton.clicked.connect(self.perform_search)
        searchLayout.addWidget(searchButton)
        
        layout.addLayout(searchLayout)
        
        self.table = ClickableTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
    def updateCompleter(self):
        field = self.fieldComboBox.currentText()
        values = list({movie.get(field, "") for movie in self.movies if movie.get(field, "")})
        completer = QCompleter(values)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchEdit.setCompleter(completer)
        
    def perform_search(self):
        query = self.searchEdit.text().lower()
        field = self.fieldComboBox.currentText()
        filtered = [movie for movie in self.movies if query in movie.get(field, "").lower()]
        self.populate_table(filtered)
        
    def populate_table(self, movies):
        if not movies:
            self.table.setRowCount(0)
            return
        headers = list(movies[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(movies))
        self.table.setHorizontalHeaderLabels(headers)
        for row_index, movie in enumerate(movies):
            for col_index, header in enumerate(headers):
                value = movie.get(header, "")
                item = QTableWidgetItem(value)
                self.table.setItem(row_index, col_index, item)
        self.table.resizeColumnsToContents()

# --- Halaman REKOMENDASI: Menampilkan 5 film acak dan tombol "Random" ---
class ForYourPage(QWidget):
    def __init__(self, movies):
        super().__init__()
        self.movies = movies
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        titleLabel = QLabel("Rekomendasi Untuk Anda")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titleLabel)
        
        randomButton = QPushButton("Random")
        randomButton.clicked.connect(self.load_random)
        layout.addWidget(randomButton)
        
        self.table = ClickableTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.load_random() 
        
    def load_random(self):
        if self.movies:
            selection = random.sample(self.movies, min(5, len(self.movies)))
            self.populate_table(selection)
        else:
            self.table.setRowCount(0)
            
    def populate_table(self, movies):
        if not movies:
            self.table.setRowCount(0)
            return
        headers = list(movies[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(movies))
        self.table.setHorizontalHeaderLabels(headers)
        for row_index, movie in enumerate(movies):
            for col_index, header in enumerate(headers):
                value = movie.get(header, "")
                item = QTableWidgetItem(value)
                self.table.setItem(row_index, col_index, item)
        self.table.resizeColumnsToContents()

# --- Halaman FILM TERATAS: Menampilkan data film secara terurut (misal berdasarkan judul) ---
class TopMoviePage(QWidget):
    def __init__(self, movies):
        super().__init__()
        self.movies = movies
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        titleLabel = QLabel("Film Teratas")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titleLabel)
        
        self.table = ClickableTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        sorted_movies = sorted(self.movies, key=lambda m: m.get("title", ""))
        self.populate_table(sorted_movies)
        
    def populate_table(self, movies):
        if not movies:
            self.table.setRowCount(0)
            return
        headers = list(movies[0].keys())
        self.table.setColumnCount(len(headers))
        self.table.setRowCount(len(movies))
        self.table.setHorizontalHeaderLabels(headers)
        for row_index, movie in enumerate(movies):
            for col_index, header in enumerate(headers):
                value = movie.get(header, "")
                item = QTableWidgetItem(value)
                self.table.setItem(row_index, col_index, item)
        self.table.resizeColumnsToContents()

# --- Halaman RINGKASAN: Menampilkan informasi ringkasan data film ---
class SummaryPage(QWidget):
    def __init__(self, movies):
        super().__init__()
        self.movies = movies
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        titleLabel = QLabel("Ringkasan Film")
        titleLabel.setAlignment(Qt.AlignCenter)
        titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(titleLabel)
        
        total = len(self.movies)
        summaryLabel = QLabel(f"Total Film: {total}")
        summaryLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(summaryLabel)
        self.setLayout(layout)

# --- Main Window dengan Menu Utama ---
class MovieTubiWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Movie Tubi")
        self.setGeometry(100, 100, 800, 600)
        
        self.movies = load_csv_data_from_file()
        
        self.initUI()
        
    def initUI(self):
        self.stackedWidget = QStackedWidget()
        self.pages = {}
        self.pages["Home"] = HomePage(self.movies)
        self.pages["Search"] = SearchPage(self.movies)
        self.pages["ForYourPage"] = ForYourPage(self.movies)
        self.pages["TopMovie"] = TopMoviePage(self.movies)
        self.pages["Summary"] = SummaryPage(self.movies)
        
        for page in self.pages.values():
            self.stackedWidget.addWidget(page)
            
        self.setCentralWidget(self.stackedWidget)
        self.create_menu()
        
    def create_menu(self):
        menubar = self.menuBar()
        
        homeAction = QAction("Home", self)
        homeAction.triggered.connect(lambda: self.switch_page("Home"))
        
        searchAction = QAction("Cari", self)
        searchAction.triggered.connect(lambda: self.switch_page("Search"))
        
        forYourPageAction = QAction("Rekomendasi", self)
        forYourPageAction.triggered.connect(lambda: self.switch_page("ForYourPage"))
        
        topMovieAction = QAction("Film Teratas", self)
        topMovieAction.triggered.connect(lambda: self.switch_page("TopMovie"))
        
        summaryAction = QAction("Ringkasan", self)
        summaryAction.triggered.connect(lambda: self.switch_page("Summary"))
        
        menubar.addAction(homeAction)
        menubar.addAction(searchAction)
        menubar.addAction(forYourPageAction)
        menubar.addAction(topMovieAction)
        menubar.addAction(summaryAction)
        
    def switch_page(self, page_name):
        page = self.pages.get(page_name)
        if page:
            self.stackedWidget.setCurrentWidget(page)

# --- Eksekusi Aplikasi ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovieTubiWindow()
    window.show()
    sys.exit(app.exec_())
