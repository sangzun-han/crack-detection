const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const table = document.querySelector(".origin-table");
const page = document.querySelector(".page");
const tbody = document.querySelector(".table-body");
const result = document.querySelector(".result");
tableOutput.style.display = "none";

searchField.addEventListener("keyup", (event) => {
  const searchValue = event.target.value;
  if (searchValue.trim().length > 0) {
    page.style.disply = "none";
    tbody.innerHTML = "";
    fetch("/search", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        table.style.display = "none";
        tableOutput.style.display = "block";

        if (data.length === 0) {
          result.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          result.style.display = "none";
          data.map((item) => {
            if (item.isFlattened == true) {
              item.isFlattened = "O";
            } else {
              item.isFlattened = "X";
            }

            tbody.innerHTML += `
              <tr>
              <td scope="row">${item.id}</td>
              <td>
               <a href=""><img src="/media/${item.image}" alt="image" style="width: 200px" /></a>
              </td>
              <td>${item.category_name}</td>
              <td>${item.state}</td>
              <td>${item.cause}</td>
              <td>${item.solution}</td>
              <td>${item.isFlattened}</td>
              </tr>
            `;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    table.style.display = "table";
    page.style.disply = "block";
    result.style.display = "none";
  }
});
