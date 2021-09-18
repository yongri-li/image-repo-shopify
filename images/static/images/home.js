

document.addEventListener('DOMContentLoaded', function () {
    //GET a list of images
    //const repoList = document.querySelector('#repo-list')
    const repoStatic = document.querySelector('#repo-static')

    let selectOption = document.createElement("select");
    let option0 = document.createElement("option");
    option0.setAttribute("value","public")
    option0.innerText = "Public"
    let option1 = document.createElement("option");
    option1.setAttribute("value","private")
    option1.innerText = "Private"
    let option2 = document.createElement("option");
    option2.setAttribute("value","both")
    option2.innerText = "All"

    selectOption.append(option2)
    selectOption.append(option1)
    selectOption.append(option0)

    let selected = document.createElement("button");
    selected.innerHTML = `Submit`
    selected.addEventListener('click', function() {
        //console.log(selectOption.value)
        loadRepos(selectOption.value)
    })
    repoStatic.append(selectOption)
    repoStatic.append(selected)
    loadRepos("both")


    
    
})

loadRepos = function(level) {
    fetch(`/images/${level}`)
    .then(response => response.json())
    .then(repos => {
        const repoList = document.querySelector('#repo-list')
        repoList.innerHTML = ""
        //console.log(repos)
        for (let i = 0; i < repos.length; i++) {
            let box = document.createElement('div');
            box.style.float = "left"

            let newContent = document.createElement('div');
            newContent.style.borderStyle = "groove"
            newContent.style.float = "right"
            newContent.style.margin = "10px"
            let theImage = document.createElement('img');
            let title = document.createElement("h3");
            let des = document.createElement("p");

            title.innerHTML = repos[i].title;

            des.innerText = repos[i].description;

            theImage.setAttribute("src", repos[i].thumbnail);
            theImage.setAttribute("alt", repos[i].title);
            theImage.setAttribute("height", "100");

            let label = document.createElement("label");
            label.setAttribute("for",repos[i].title);

            let check = document.createElement("input");
            check.setAttribute("type", "checkbox");
            check.setAttribute("id",repos[i].title);
            //check.setAttribute("value","yes");
            check.setAttribute("name","repo");

            label.append(check);

            let author = document.createElement("h5");
            author.innerHTML = `by ${repos[i].author} on ${repos[i].timestamp}`

            //box.append("HELLO")
            box.append(label);
            newContent.append(title);
            //newContent.append(label);
            newContent.append(theImage);
            newContent.append(des);
            newContent.append(author);
            box.append(newContent);


            newContent.addEventListener('click', () => {
                console.log(`YOU JUST CLICKED ${repos[i].title} with the id of ${repos[i].id}`);
                window.location.href = `/detail/${repos[i].id}`;
            })


            repoList.append(box);
        }
    })
}