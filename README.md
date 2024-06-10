# Django API Project

This project is a Django-based API with models for `Item` and `Supplier`, and includes viewsets for managing these resources. Below are the steps to set up and get things running.

## Getting Started

### Prerequisites

- Python 3.11+
- Git
- Virtualenv (optional but recommended)

### Setup Instructions

1. **Clone the Repository**

    ```sh
    git clone https://github.com/TangoIndiaMango/inventory_management.git
    cd inventory_management
    ```

2. **Set Up a Virtual Environment**

    It's recommended to use a virtual environment to manage dependencies. You can set one up using `virtualenv`:

    ```sh
    python3 -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. **Install the Requirements**

    Install the required packages using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set Up the Database**

    Apply the migrations to set up the database schema:

    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run the Server**

    Start the development server:

    ```sh
    python manage.py runserver
    ```

    The API should now be accessible at `http://127.0.0.1:8000/`.

### Testing the API

1. **Import Postman Collection**

    - Open Postman.
    - Import the provided Postman collection (usually a `.json` file).
    - The collection contains pre-configured requests to test your API endpoints.

2. **Run Tests**

    You can run the tests using the following command:

    ```sh
    python manage.py test
    ```

## API Endpoints

Here are some example endpoints you can test using Postman or other HTTP clients:

- **Suppliers**
    - `GET /api/inventory/suppliers/` - List all suppliers
    - `POST /api/inventory/suppliers/` - Create a new supplier
    - `GET /api/inventory/suppliers/{id}/` - Retrieve a specific supplier
    - `PUT /api/inventory/suppliers/{id}/` - Update a specific supplier
    - `DELETE /api/inventory/suppliers/{id}/` - Delete a specific supplier


- **Items**
    - `GET /api/inventory/items/` - List all items
    - `POST /api/inventory/items/` - Create a new item
    - `GET /api/inventory/items/{id}/` - Retrieve a specific item
    - `PUT /api/inventory/items/{id}/` - Update a specific item
    - `DELETE /api/inventory/items/{id}/` - Delete a specific item



## Contact

For any questions, please contact [Aliyu Timilehin](https://www.linkedin.com/in/timilehin-aliyu).