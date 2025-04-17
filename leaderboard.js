function back() {
    window.location.href = "index.html";
}

const baseUrl = "http://172.26.103.14:8080";

async function httpGet(theUrl) {
    try {
        const response = await fetch(theUrl);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
}

async function getUserData(username) {
    const url = `${baseUrl}/users/${username}`; 
    return await httpGet(url);
}

const username = "a"; 

getUserData(username)
    .then(response => {
        const x = document.getElementById("lb");
        x.innerHTML = "<div class='leader'><p>" + JSON.stringify(response) + "</p></div>";
    })
    .catch(error => {
        console.error('Error fetching user data:', error);
    });