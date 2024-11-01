# Rubidium

An interactive football simulator using FIFA24 (FC24) data and analytics

<p align=”center”>
<img width="1000" src="https://raw.githubusercontent.com/xylium117/rubidium/refs/heads/master/banner.png" alt="Banner">
</p>

---
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)&nbsp;
![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)&nbsp;
[![License: MIT](https://img.shields.io/badge/LICENSE-GPL_3.0-green?style=for-the-badge)](https://github.com/xylium117/pavillion/blob/master/LICENSE.md)


## Table of Contents 📜

- Overview 🌟
- Features 📂
- Getting Started 🚀
- Contributing 🤝
- Roadmap 📈
- License 📝

## Getting Started 🚀

```bash
git clone https://github.com/xylium117/rubidium.git
```
Then proceed open the directory.
```bash
cd rubidium
```
Setup and activate virtual environment (optional)
```bash
# To create a virtual env:
python -m venv .venv

# For activation use one of the following commands based on your OS:
source .venv/bin/activate   # On Mac / Linux
.venv\Scripts\activate.bat  # In Windows CMD
.venv\Scripts\Activate.ps1  # In Windows PowerShell
```
Install the required packages from the `requirements.txt` file
```bash
pip install -r requirements.txt
```

Execute the program
```bash
python simulator
```

View all data
```bash
cd simulator
python viewdata.py
```

### Prerequisites 📋

To run Rubidium, [Python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe) must be downloaded. An IDE is also suggested if you want to contribute to the code. 🏗️

## Contributing 🤝

Contributions are welcome! If you have any improvements, bug fixes, or new projects to add to this gallery, please follow these steps:

1. Fork this repository.
2. Create a new branch for your feature (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m 'Add new project'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a pull request and describe your changes. 🚀🔗

## Roadmap 📈

- [x] Add trackers for season and match analytics
- [x] Update player roster with custom players
- [x] Add preliminary data visualization
- [x] Improve UI and UX
- [x] Add viewall.py script
- [x] Implement fuzzy matching to improve UX
- [x] Add more Leagues and update player roster
- [ ] Finalise data visualisation and viewall.py script
- [ ] Improve Match mechanics (Yellow Cards, Substitutions)
- [ ] Player stats dump and career regression
- [ ] Implement tournaments
   - [ ] World Cup
   - [ ] UCL
- [ ] Implement international matches

See the [open issues](https://github.com/xylium117/rubidium/issues) for a full list of proposed features (and known issues).

## License 📝

This repository is licensed under the [GPL License](LICENSE.md). Feel free to use and modify the code as you see fit. 

---
Enjoy simulating Test matches! Cheers! 🍻
