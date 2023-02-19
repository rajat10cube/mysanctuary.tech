// const queryString = window.location.search;
// console.log(queryString);
const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const curr_username = urlParams.get('username')

console.log(curr_username);
document.getElementById("username_text1").innerHTML = curr_username;
document.getElementById("username_text2").innerHTML = curr_username;
const getVents = async () => {
    const response = await fetch('http://127.0.0.1:5000/vents',{
        headers: {
            'Access-Control-Allow-Origin': '*'
          }
    });
    const myJson = await response.json(); 
    console.log(myJson)
    post_vent = document.getElementById("post_vent")
    for(i=0;i<myJson.length;i++){
        post_vent.innerHTML += `<div style="margin-bottom:6vh"><div class="container">
        <div class="row">
            <div class="col-10" id="post_title">`+
            myJson[i].post_content+
            `</div>
            <div class="col-1 offset-1">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" style="color: white;"
                    fill="currentColor" class="bi bi-heart" viewBox="0 0 16 16">
                    <path
                        d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 7.824 1.143c.06.055.119.112.176.171a3.12 3.12 0 0 1 .176-.17C12.72-3.042 23.333 4.867 8 15z" />
                </svg>
            </div>
        </div>
        <div class="d-flex flex-row" id="post_tags">
            <div class="p2 tag-text">`
            +
            myJson[i].topics
            +`</div>
            <div class="p2 tag-text">`
            +
            myJson[i].emotion
            +`</div>
        </div>
        <div class="row">
            <div class="col-1">
                <img class="user-image" width="35vh" src="images/memoji_boys_3_15.png">
            </div>
            <div class="col-2">
                <div class="row">
                    <div class="col-12 username-text">`+
                    myJson[i].username+`
                    </div>
                    <div class="col-12 date-text">
                        02/19/2013
                    </div>
                </div>
            </div>
            <div class="col-2 offset-5 likes-text">
                231 Likes
            </div>
            <div class="col-2 comments-text">
                21 Comments
            </div>
        </div>
    </div></div>`
    }
}

const postVent = async () => {
    post_content = document.getElementById("postVent").value;
    const response = await fetch('http://127.0.0.1:5000/vents', {
      method: 'POST',
      body: JSON.stringify({"username":curr_username, "post_content":post_content}), // string or object
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
    const myJson = await response.json(); //extract JSON from the http response

}

getVents();
const createPost = async ()=>{
    post_content = document.getElementById("postVent").value;
    const response = await fetch('http://127.0.0.1:5000/vents', {
      method: 'POST',
      body: JSON.stringify({"username":curr_username, "post_content":post_content}), // string or object
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
    const myJson = await response.json(); //extract JSON from the http response
    console.log(myJson)
}