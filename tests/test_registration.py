import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Fixture untuk menyiapkan database sebelum pengujian dan membersihkannya setelah selesai."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Fixture untuk mendapatkan koneksi database dan menutupnya setelah pengujian."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Menguji pembuatan database dan tabel pengguna."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Tabel 'users' harus ada dalam database."

def test_add_new_user(setup_database, connection):
    """Menguji penambahan pengguna baru."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Pengguna harus ditambahkan ke database."

# Berikut adalah pengujian yang bisa ditulis:
"""
Menguji percobaan menambahkan pengguna dengan nama pengguna yang sudah ada.
Menguji keberhasilan autentikasi pengguna.
Menguji autentikasi pengguna yang tidak ada.
Menguji autentikasi dengan kata sandi yang salah.
Menguji tampilan yang benar dari daftar pengguna.
"""