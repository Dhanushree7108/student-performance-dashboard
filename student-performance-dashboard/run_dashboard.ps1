Set-Location "C:\Users\dhanu\Downloads\student-performance-dashboard (2)\student-performance-dashboard"
$python = "C:\Users\dhanu\AppData\Local\Programs\Python\Python312\python.exe"
& $python -m streamlit run dashboard/app.py --server.headless true --server.port 8502
