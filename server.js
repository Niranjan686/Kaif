const express = require("express");
const { exec } = require("child_process");
const path = require("path");

const app = express();
const PORT = 3000;

// Serve static files (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, "public")));

// API route to call Python AI function
app.get("/Spotify", (req, res) => {
    exec("streamlit run Spotify.py", { encoding: "utf-8" }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        console.log(`Output: ${stdout}`);
    });
});
app.get("/Youtube", (req, res) => {
    exec("streamlit run Youtube.py", { encoding: "utf-8" }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        console.log(`Output: ${stdout}`);
    });
});
app.get("/Handracking", (req, res) => {
    exec("streamlit run handracking.py", { encoding: "utf-8" }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        console.log(`Output: ${stdout}`);
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
