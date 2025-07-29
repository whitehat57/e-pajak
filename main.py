#!/usr/bin/env python3
"""
Tax Manager - Aplikasi CLI untuk mengelola kewajiban perpajakan
"""

from ui.dashboard import TaxDashboard

def main():
    """Entry point aplikasi"""
    try:
        dashboard = TaxDashboard()
        dashboard.run()
    except KeyboardInterrupt:
        print("\n\n👋 Aplikasi dihentikan oleh pengguna")
    except Exception as e:
        print(f"\n❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()