from setuptools import setup


def main():
    setup(setup_requires=["setuptools-odoo"], odoo_addon=True)


if __name__ == "__main__":
    main()
