
function addCourse() {
    var courseName = document.getElementById("courseName").value;
    var location = document.getElementById("location").value;
    var time = document.getElementById("time").value;
    
    var days = [];
    document.querySelectorAll('input[name="day"]:checked').forEach((checkbox) => {
        days.push(checkbox.value);
    });

    console.log(courseName);
    console.log(location);
    console.log(time);
    console.log(days);

    var table = document.getElementById("courseTable");
    var newRow = table.insertRow();

    var cell1 = newRow.insertCell(0);
    var cell2 = newRow.insertCell(1);
    var cell3 = newRow.insertCell(2);
    var cell4 = newRow.insertCell(3);

    cell1.innerHTML = courseName;
    cell2.innerHTML = location;
    cell3.innerHTML = time;
    cell4.innerHTML = days.join(", ");

    // Clear the form fields
    document.getElementById("courseForm").reset();
}