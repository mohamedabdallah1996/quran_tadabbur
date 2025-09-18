# Quran Tadabbur

Quran Tadabbur is a FastAPI-based application that provides a Quranic verse search and retrieval system. It uses PostgreSQL for structured data storage and Qdrant for vector-based similarity search. The application also integrates with Sentence Transformers to generate embeddings for Quranic verses and their translations.

---

## Features

- Retrieve Quranic verses by ID, Surah number, or Surah name.
- Perform vector-based similarity searches using Qdrant.
- Populate the database with Quranic verses from a dataset.
- RESTful API endpoints for easy integration.

---

## Prerequisites

- Docker and Docker Compose installed.
- Python 3.11 installed (if running locally without Docker).

---

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/quran-tadabbur.git
cd quran-tadabbur
```

### 2. Configure Environment Variables

Edit the `.env` file to set the required environment variables:

### 3. Build and Run with Docker

#### a. Start the Services

```bash
docker-compose up --build
```

This will start the following services:
- **PostgreSQL**: Database for structured data.
- **Qdrant**: Vector database for similarity search.
- **FastAPI**: The main application.
- **PgAdmin**: Web-based database management tool.

#### b. Access the Application

- FastAPI: [http://localhost:8000](http://localhost:8000)
- PgAdmin: [http://localhost:5050](http://localhost:5050) (Default credentials: `admin@admin.com` / `admin`)

---

## Running Locally Without Docker

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize the Database

Run the SQL script to create the database:

```bash
psql -U postgres -f init.sql
```

### 3. Start the Application

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

---

## API Endpoints

### Base URL: `/verses`

#### 1. Get Verse by ID
- **GET** `/verses/{verse_id}`
- **Response**: Single verse details.

#### 2. Get Verses by Surah Number
- **GET** `/verses/surah_number/{surah_number}`
- **Response**: List of verses in the specified Surah.

#### 3. Get Verses by Surah Name
- **GET** `/verses/surah_name/{surah_name}`
- **Response**: List of verses in the specified Surah.

---

## Dataset

The application uses the Quran dataset from the [Hugging Face Datasets library](https://huggingface.co/datasets/ReySajju742/Quran). The dataset is automatically loaded and ingested into the database and Qdrant during the application startup.

---

## Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Ensure PostgreSQL is running and the credentials in `.env` are correct.
   - If running locally, set `POSTGRES_HOST=localhost`.

2. **Qdrant Connection Error**:
   - Ensure Qdrant is running and accessible at the specified host and port.

3. **Dataset Not Found**:
   - Ensure the dataset is available in the Hugging Face Datasets library.

---

## License

This project is licensed under the MIT License.

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## Contact

For any questions or support, please contact [your-email@example.com].