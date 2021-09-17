

console.log("HELLO")
document.addEventListener('DOMContentLoaded', function() {

    const imageList = document.querySelector('#image-list')
    const repoID = document.URL.split("/")[document.URL.split("/").length-1]
    
    fetch(`/repo_details/${repoID}`)
    .then(response => response.json())
    .then(details => {
        console.log(details)
    })
    
    //console.log("HEHLDFDF")
    //fetch(`/detail/${repoID}`)


})
