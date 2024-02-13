# Personal Finance Tracker

Personal Finance Tracker (PFT) is a web application designed to help users manage their finances with ease. With PFT, users can track their spending, record transactions, generate reports, and set and monitor saving goals.

## Key Features

- **Dashboard**: Provides an overview of the user's financial status, including net cash flow, income, and expenses.
- **Transaction Records**: Allows users to add, edit, and delete income and expense records.
- **Reports**: Users can view detailed monthly and daily transaction reports and set preferences for receiving these reports via email.
- **Saving Goals**: Users can create, edit, and track progress towards their financial saving goals.

## Installation and Setup

To get the application running locally on your system, please follow the steps below:

1. Clone the repository to your local machine.
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   ```
2. Navigate to the application directory.
   ```bash
   cd your-repo-name
   ```
3. Install the required dependencies.
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your environment variables by creating a `.env` file based on the `.env.example` provided.
5. Initialize the database with the following commands:
   ```bash
   flask db upgrade
   ```
6. Start the application.
   ```bash
   flask run
   ```

## Usage

After starting the application, you can access the following endpoints on your local server:

- Home: `/`
- Dashboard: `/dashboard`
- Transaction Records: `/transactions`
- Reports: `/reports`
- Saving Goals: `/saving-goals`

You can register a new account or log in using existing credentials to start using the application.

## Technologies

- **Flask**: A micro web framework written in Python.
- **SQLAlchemy**: An SQL toolkit and ORM for Python.
- **Celery**: An asynchronous task queue/job queue.
- **Flask-WTF**: Simple integration of Flask and WTForms, including CSRF protection.
- **SQLite**: Used for the development database.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name – [@your_twitter](https://twitter.com/your_twitter) - email@example.com

Project Link: [https://github.com/your-username/your-repo-name](https://github.com/your-username/your-repo-name)

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc.
