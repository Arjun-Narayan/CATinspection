import express from "express";
import bodyParser from "body-parser";
import morgan from "morgan";

const app = express();
const port = 3000;
app.use(bodyParser.urlencoded({extended: true}));
app.use(express.static("public"));
app.use(morgan("dev"));

app.listen(port, () => {
    console.log("Server running on port " + port);
});

app.get("/", (req, res) =>{
    res.render("index.ejs", {
        cssFiles: ["css/header.css", "css/index.css", "css/footer.css"],
        runningInspection: 0,
        allInspections: [
            {
                id: 1,
                type: "truck",
                model: "v1",
                date: new Date(),
                location: "India",
            }
        ],
        username: "a",
    });
});

app.get("/inspectionStart", (req, res) =>{
    res.render("inspectionStart.ejs", {
        cssFiles: ["css/header.css", "css/inspectionstart.css", "css/footer.css"],
        runningInspection: 1,
    })
})