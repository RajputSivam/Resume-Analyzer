# Resume Analyzer

A web-based Resume Analyzer that helps users analyze their resumes and get useful insights about their content, skills, and overall resume quality.

## 🚀 Features

* 📄 Upload and analyze resumes
* 🔍 Extract useful information from resumes
* 🧠 Analyze resume content
* 💼 Identify skills and relevant keywords
* 📊 Provide resume analysis/results
* 🔐 User authentication
* 👤 User registration and login
* 💾 Store user-related information
* 🌐 Responsive web interface

## 🛠️ Technologies Used

### Frontend

* React.js
* JavaScript
* HTML5
* CSS3
* Axios

### Backend

* Node.js
* Express.js
* REST API
* JWT Authentication

### Database

* MongoDB

### Other Tools

* Git & GitHub
* VS Code
* npm

## 📁 Project Structure

```text
Resume-Analyzer/
│
├── client/                 # Frontend
│   ├── src/
│   ├── public/
│   └── package.json
│
├── server/                 # Backend
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── middleware/
│   ├── config/
│   └── package.json
│
├── .gitignore
└── README.md
```

> The exact folder structure may vary depending on your implementation.

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/RajputSivam/Resume-Analyzer.git
```

### 2. Navigate to the Project

```bash
cd Resume-Analyzer
```

### 3. Install Dependencies

If the project has separate frontend and backend folders:

```bash
cd client
npm install
```

Then:

```bash
cd ../server
npm install
```

## 🔑 Environment Variables

Create a `.env` file in the backend directory and add the required environment variables.

Example:

```env
PORT=5000
MONGO_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
```

Do not upload your `.env` file to GitHub.

## ▶️ Running the Project

### Start Backend

```bash
cd server
npm start
```

or, if using nodemon:

```bash
npm run dev
```

### Start Frontend

Open another terminal:

```bash
cd client
npm start
```

The application will then be available locally in your browser.

## 🔄 How It Works

1. User creates an account or logs in.
2. User uploads their resume.
3. The application processes the resume.
4. Resume information is analyzed.
5. The system identifies relevant skills and keywords.
6. Analysis results are displayed to the user.
7. Users can use the feedback to improve their resume.

## 🎯 Project Objective

The main objective of Resume Analyzer is to provide an easy-to-use platform that helps users understand how effectively their resume represents their skills and experience.

It can help users identify missing information, relevant keywords, and areas where their resume can be improved.

## 🔮 Future Improvements

* ATS score calculation
* AI-powered resume recommendations
* Job description matching
* Resume keyword optimization
* Multiple resume format support
* Resume improvement suggestions
* Job recommendation system
* PDF report generation

## 👨‍💻 Author

Developed as a B.Tech Computer Science Engineering project.

## 📄 License

This project is intended for educational and portfolio purposes.
