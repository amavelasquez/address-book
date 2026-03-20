# Clone repository
```
$ git clone https://github.com/amavelasquez/address-book.git
```

# Navigate to root of directory 
```
$ cd repo
```

# Repository should look like this
.
├── app/
├── LICENSE
├── README.md
└── requirements.txt

# Install required libraries using the following command
```
$ pip install -r requirements.txt
```

# Navigate to the app folder
```
$ cd app
```

# Repository should look like this
app
├── db/
├── models/
├── utils/
├── address.db
└── main.py

# Run the app
```
$ uvicorn main:app --reload
```