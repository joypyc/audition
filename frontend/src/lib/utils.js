export function getCookie(cookieName) {
    // Split the document.cookie string into individual cookies
    const cookiesArray = document.cookie.split('; ');

    // Loop through each cookie to find the one with the specified name
    for (let i = 0; i < cookiesArray.length; i++) {
        const cookie = cookiesArray[i];
        // Split the cookie into name and value
        const [name, value] = cookie.split('=');
        // Check if the name matches the provided cookieName
        if (name === cookieName) {
            // Return the value of the cookie
            return decodeURIComponent(value);
        }
    }
    // Return null if cookie not found
    return null;
}

export function fillUrl(params,url){
    for(const [key,val] of Object.entries(params)){
        if(typeof(key) === 'string' && typeof(val) === 'string'){
            url = url.replace(`{${key}}`,val);
        }        
    }
    return url;
}


export function capitalizeWords(str) {
    // Split the string into words
    let words = str.split(' ');

    // Capitalize the first letter of each word
    for (let i = 0; i < words.length; i++) {
        words[i] = words[i].charAt(0).toUpperCase() + words[i].slice(1);
    }

    // Join the words back together
    return words.join(' ');
}

export function getValues(options){
    let values = []
    for (let [field,val] of Object.entries(options)){
        values.push(val)
    }
    return values
}