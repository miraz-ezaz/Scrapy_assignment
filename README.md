# Scrapy Hotel Spider

This project is a web scraping application built using Scrapy. It scrapes hotel information from Trip.com, including hotel names, locations, ratings, room types, prices, and images. The images are downloaded and saved with a custom naming convention, and all data is stored in a PostgreSQL database.

## Features

- **Scrapes Hotel Data**: Extracts hotel names, locations, ratings, room types, prices, and images from Trip.com.
- **Image Downloading**: Downloads hotel images and saves them with custom file names based on the hotel name, room type, and image index.
- **Database Storage**: Stores the scraped data in a PostgreSQL database.
- **POST Request Handling**: Initiates scraping with a POST request to retrieve dynamic content.
- **Automatic Database Setup**: The database and tables are created automatically if they do not exist.

## Project Structure

```plaintext
Scrapy_assignment/
├── hotel_spider/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       ├── __init__.py
│       └── hotels.py
├── database_manager/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
├── images/
│   └── [Downloaded images will be saved here]
├── scrapy.cfg
└── README.md
```

## Installation

### Prerequisites

- Python 3.7 or higher
- PostgreSQL
- Scrapy
- Pillow (for image processing)
- SQLAlchemy
- Docker (optional, for running PostgreSQL locally)

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/miraz-ezaz/Scrapy_assignment.git
   cd Scrapy_assignment
   ```

2. **Set up a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**:

   Create a `.env` file in the `database_manager` directory with the following content:

   ```plaintext
   DATABASE_URL=postgresql://your_username:your_password@localhost:5432/hotel_data
   ```

   Replace `your_username`, `your_password`, `localhost`, and `hotel_data` with your actual PostgreSQL credentials and database information. The database and tables will be created automatically if they do not exist.

5. **Navigate to the `hotel_spider` directory**:

   Before running the spider, navigate to the `hotel_spider` directory:

   ```bash
   cd hotel_spider
   ```

6. **Run the spider**:

   ```bash
   scrapy crawl hotels
   ```

   The database and tables will be created automatically if they do not exist.

## Usage

### Custom Image Naming

Images are downloaded and saved with the naming convention `hotel_name_room_type_index.jpg`. For example:

```plaintext
images/
└── Grand_Hotel_Deluxe_Room_1.jpg
└── Grand_Hotel_Deluxe_Room_2.jpg
```

### Database Storage

The scraped data is stored in a PostgreSQL database. The data includes the hotel name, location, rating, room type, price, and paths to the downloaded images.

### Automatic Database Setup

The database and tables will be automatically created when you run the spider if they do not already exist. The configuration for the database connection is provided in the `.env` file using the `DATABASE_URL`.

## Configuration

### Scrapy Settings

The Scrapy settings for the project are configured in `hotel_spider/settings.py`. Important settings include:

- **IMAGES_STORE**: Directory where images are stored.
- **ITEM_PIPELINES**: Pipeline configuration to enable the custom image pipeline and database storage.

### Database Configuration

The database configuration is handled by the `database_manager` package. The database is initialized in `database.py`, and the models are defined in `models.py`.

## Troubleshooting

- **Images Not Downloading**: Ensure that the `IMAGES_STORE` directory is correctly set in `settings.py` and that the pipeline is enabled.
- **Database Connection Issues**: Verify the PostgreSQL connection details in the `.env` file and ensure that the database server is running.

 
