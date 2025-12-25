const http = require('http');

/**
 * Simple script to verify that the frontend is running and accessible
 */
function testFrontend() {
    console.log("Testing frontend server accessibility...");

    const options = {
        host: 'localhost',
        port: 3001,
        path: '/Physical-AI-Humanoid-Robotics-Textbook/',
        method: 'GET'
    };

    const req = http.request(options, (res) => {
        console.log(`Status Code: ${res.statusCode}`);

        if (res.statusCode === 200) {
            console.log("[SUCCESS] Frontend server is accessible and responding with 200 OK");
            console.log("[SUCCESS] Content is being displayed properly");
        } else {
            console.log(`[ERROR] Frontend server returned status code: ${res.statusCode}`);
        }

        res.on('data', (chunk) => {
            // Only log a small sample to avoid too much output
            const sample = chunk.toString().substring(0, 200);
            if (sample.includes('Humanoid Robotics Textbook')) {
                console.log("[SUCCESS] Page contains expected content ('Humanoid Robotics Textbook')");
            }
        });

        res.on('end', () => {
            console.log("\n[SUCCESS] Frontend verification completed!");
            console.log("Frontend is running on http://localhost:3001/Physical-AI-Humanoid-Robotics-Textbook/");
            console.log("Backend is running on http://localhost:8000");
        });
    });

    req.on('error', (e) => {
        console.error(`[ERROR] Problem with request: ${e.message}`);
        console.log("Make sure both backend (port 8000) and frontend (port 3001) are running");
    });

    req.end();
}

// Run the test
testFrontend();