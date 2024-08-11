import express from "express";
import bodyParser from "body-parser";
import morgan from "morgan";
import spawn from "cross-spawn";

const app = express();
const port = 4000;
app.use(bodyParser.json());
app.use(morgan("dev"));

var allInspections = [];
class inspection{
    static numberOFInspections = 1;
    constructor(id, userID, serialno, modelno, location, date, pdfPath){
        this.id = id;
        this.userID = userID;
        this.serialno = serialno;
        this.modelno = modelno;
        this.location = location;
        this.date = new Date().toDateString() + " " + new Date().toTimeString();
        this.pdfPath = pdfPath;
        inspection.numberOFInspections++;
    }
}

app.listen(port, () =>{
    console.log("Server running on port " + port);
});

app.get("/inspectionID", (req, res) =>{
    res.json({
        count: inspection.numberOFInspections,
    });
});

app.post("/getInspections", (req, res) =>{
    const userID = req.body.uid;
    const allUserInspections = allInspections.filter((inspection) => inspection.userID === userID);
    res.json({
        "content" : allUserInspections,
    });
});

app.post("/addInspection", (req, res) =>{
    const newInspection = (JSON.parse(req.body.inspection)).header;
    let id = inspection.numberOFInspections;
    let userid = "Inspector Unique ID";//fetch from caterpillar database
    let serialNum = newInspection.truck_serial_number;
    let modelNum = newInspection.truck_model;
    let location = newInspection.location;
    let pdfPath = "abc";
    const addedInspection = new inspection(id, userid, serialNum, modelNum, location, pdfPath);
    allInspections.push(addedInspection);
    console.log(allInspections);
    res.json({
        content: "sent successfully",
    });
});

app.post("/getSummary", (req, res) =>{
    const componentDetails = req.body.content;
    const process = spawn('python', ["LLM/report_generation.py", componentDetails]);
    process.stdout.on('data', function(data){
        res.json({
            content: data.toString(),
        });
    });
});

app.post("/generateReport", (req, res) =>{
    const summary = req.body['inspectionSummary'];
    const process = spawn('python', ["LLM/final_report.py", summary]);
    process.stdout.on('data', function(data){
        res.json({
            content: data.toString(),
        });
    });
});

app.get("/", (req, res) =>{
    const process = spawn('python', ["LLM/final_report.py"]);
    process.stdout.on('data', function(data){
        console.log("data sent");
        res.json({
            content: data.toString(),
        });
    });
})