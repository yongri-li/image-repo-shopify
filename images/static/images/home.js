

document.addEventListener('DOMContentLoaded', function () {
    const repoStatic = document.querySelector('#repo-static')

    let selectOption = document.createElement("select");
    selectOption.setAttribute("class","form-select");
    let option0 = document.createElement("option");
    option0.setAttribute("value","public")
    option0.innerText = "Public"
    let option1 = document.createElement("option");
    option1.setAttribute("value","private")
    option1.innerText = "Private"

    selectOption.append(option0)
    selectOption.append(option1)
    

    let selected = document.createElement("button");
    selected.setAttribute("class","btn btn-success")
    selected.innerHTML = `Submit`
    selected.addEventListener('click', function() {
        loadRepos(selectOption.value)
    })
    repoStatic.append(selectOption)
    repoStatic.append(selected)
    loadRepos("public")


    
    
})

loadRepos = function(level) {
    fetch(`/images/${level}`)
    .then(response => response.json())
    .then(repos => {
        const repoList = document.querySelector('#repo-list')
        repoList.innerHTML = ""
        for (let i = 0; i < repos.length; i++) {

            let newContent = document.createElement('div');
            //newContent.style.borderStyle = "groove"
            newContent.setAttribute("class","card")
            newContent.setAttribute("style","padding:20px;")
            
            //newContent.style.margin = "10px"
            let theImage = document.createElement('img');
            theImage.setAttribute("class","card-img-left")
            let title = document.createElement("h3");
            title.setAttribute("class","card-title")
            let des = document.createElement("p");
            des.setAttribute("class","card-text")

            title.innerHTML = repos[i].title;

            des.innerText = repos[i].description;

            theImage.setAttribute("src", repos[i].thumbnail);
            theImage.setAttribute("alt", repos[i].title);
            theImage.setAttribute("height", "100");

            //let label = document.createElement("label");
            //label.setAttribute("for",repos[i].title);


            let author = document.createElement("h6");
            author.innerHTML = `by ${repos[i].author} on ${repos[i].timestamp}`

            newContent.append(title);
            newContent.append(theImage);
            newContent.append(des);
            newContent.append(author);


            newContent.addEventListener('click', () => {
                console.log(`YOU JUST CLICKED ${repos[i].title} with the id of ${repos[i].id}`);
                window.location.href = `/detail/${repos[i].id}`;
            })


            repoList.append(newContent);
        }
    })
}