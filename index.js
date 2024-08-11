import express from "express";
import bodyParser from "body-parser";
import morgan from "morgan";
import axios from "axios";

const app = express();
const port = 3000;
const apiURL = "http://localhost:4000/";
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static("public"));
app.use(morgan("dev"));

var currentInspection = {};
var components = ["Header", "Tires", "Battery", "Exterior", "Brakes", "Engine", "Feedback"];
var summaryList = {}

function allValuesReset() {
    var summaryList = {}
    currentInspection = {};
    components =  ["Header", "Tires", "Battery", "Exterior", "Brakes", "Engine", "Feedback"];
}

app.listen(port, () => {
    console.log("Server running on port " + port);
});

app.get("/", async (req, res) => {
    allValuesReset();
    let inspections;
    try {
        const response = (await axios({
            method: "post",
            baseURL: apiURL,
            url: "getInspections",
            responseType: "json",
            data: {
                uid: "Inspector Unique ID", //fetch from caterpillar database
            }
        })).data;
        inspections = response.content;
    } catch (error) {
        console.log(error);
    }
    res.render("index.ejs", {
        cssFiles: ["css/header.css", "css/index.css", "css/footer.css"],
        runningInspection: false,
        allInspections: inspections,
    });
});

app.get("/inspectionStart", (req, res) => {
    if (components.includes("Header")){
        res.render("inspectionStart.ejs", {
            cssFiles: ["css/header.css", "css/inspectionstart.css", "css/footer.css"],
            runningInspection: true,
        });
    } else{
        res.json({
            message: "already visited",
        });
    }
});

app.get("/componentChoice", (req, res) => {
    if (components.length === 1) {
        res.redirect("/feedback");
    } else {
        res.render("componentchoice.ejs", {
            cssFiles: ["css/header.css", "css/componentchoice.css", "css/footer.css"],
            runningInspection: true,
            components: components,
        });
    }
});

app.get("/tires", (req, res) => {
    if (components.includes("Tires")) {
        const tiresCheck = [
            {
                question: "Tire Pressure For Left Front",
                type: "number",
                photo: false,
            },
            {
                question: "Tire Pressure For Right Front",
                type: "number",
                photo: false,
            },
            {
                question: "Tire Condition For Left Front",
                type: "select",
                options: ["Good", "Ok", "Needs Replacement"],
                photo: true,
            },
            {
                question: "Tire Condition For Right Front",
                type: "select",
                options: ["Good", "Ok", "Needs Replacement"],
                photo: true,
            },
            {
                question: "Tire Pressure For Left Rear",
                type: "number",
                photo: false,
            },
            {
                question: "Tire Pressure For Right Rear",
                type: "number",
                photo: false,
            },
            {
                question: "Tire Condition For Left Rear",
                type: "select",
                options: ["Good", "Ok", "Needs Replacement"],
                photo: true,
            },
            {
                question: "Tire Condition For Right Rear",
                type: "select",
                options: ["Good", "Ok", "Needs Replacement"],
                photo: true,
            },
        ];
        res.render("componentcheck.ejs", {
            component: "Tires",
            checklist: tiresCheck,
            cssFiles: ["css/header.css", "css/componentcheck.css", "css/footer.css"],
            runningInspection: true,
        });
    } else {
        res.json({
            message: "already visited",
        });
    }
});

app.get("/battery", (req, res) => {
    if (components.includes("Battery")) {
        const batteryCheck = [
            {
                question: "Battery Make",
                type: "text",
                photo: false,
            },
            {
                question: "Battery Replacement Date",
                type: "date",
                photo: false,
            },
            {
                question: "Battery Voltage",
                type: "number",
                photo: false,
            },
            {
                question: "Battery Water Level",
                type: "select",
                options: ["Good", "Ok", "Low"],
                photo: false,
            },
            {
                question: "Battery Condition (Any Damage)",
                type: "select",
                options: ["No", "Yes"],
                photo: true,
            },
            {
                question: "Any leak or rust in battery",
                type: "select",
                options: ["No", "Yes"],
                photo: false,
            },
        ];
        res.render("componentcheck.ejs", {
            component: "Battery",
            checklist: batteryCheck,
            cssFiles: ["css/header.css", "css/componentcheck.css", "css/footer.css"],
            runningInspection: true,
        });
    } else {
        res.json({
            message: "already visited",
        });
    }
});

app.get("/exterior", (req, res) => {
    if (components.includes("Exterior")) {
        const exteriorCheck = [
            {
                question: "Rust, Dent or Damage to Exterior",
                type: "select",
                options: ["No", "Yes"],
                photo: true,
            },
            {
                question: "Oil Leak in Suspension",
                type: "select",
                options: ["No", "Yes"],
                photo: false,
            },
        ];
        res.render("componentcheck.ejs", {
            component: "Exterior",
            checklist: exteriorCheck,
            cssFiles: ["css/header.css", "css/componentcheck.css", "css/footer.css"],
            runningInspection: true,
        });
    } else {
        res.json({
            message: "already visited",
        });
    }
});

app.get("/brakes", (req, res) => {
    if (components.includes("Brakes")) {
        const brakesCheck = [
            {
                question: "Brake Fluid Level",
                type: "select",
                options: ["Good", "Ok", "Low"],
                photo: false,
            },
            {
                question: "Brake Condition For Front",
                type: "select",
                options: ["Good", "Ok", "Needs Replacement"],
                photo: false,
            },
            {
                question: "Brake Condition For Rear",
                type: "select",
                options: ["Good", "Ok", "Needs Replacement"],
                photo: false,
            },
            {
                question: "Emergency Brake",
                type: "select",
                options: ["Good", "Ok", "Low"],
                photo: false,
            },
        ];
        res.render("componentcheck.ejs", {
            component: "Brakes",
            checklist: brakesCheck,
            cssFiles: ["css/header.css", "css/componentcheck.css", "css/footer.css"],
            runningInspection: true,
        });
    } else {
        res.json({
            message: "already visited",
        });
    }
});

app.get("/engine", (req, res) => {
    if (components.includes("Engine")) {
        const engineCheck = [
            {
                question: "Rust Dent or Damage in Engine",
                type: "select",
                options: ["No", "Yes"],
                photo: true,
            },
            {
                question: "Engine Oil Condition",
                type: "select",
                options: ["Good", "Bad"],
                photo: false,
            },
            {
                question: "Engine Oil Colour",
                type: "text",
                photo: false,
            },
            {
                question: "Brake Fluid Condition",
                type: "select",
                options: ["Good", "Bad"],
                photo: false,
            },
            {
                question: "Brake Fluid Colour",
                type: "text",
                photo: false,
            },
            {
                question: "Any Oil Leak in Engine",
                type: "select",
                options: ["Yes", "No"],
                photo: false,
            },
        ];
        res.render("componentcheck.ejs", {
            component: "Engine",
            checklist: engineCheck,
            cssFiles: ["css/header.css", "css/componentcheck.css", "css/footer.css"],
            runningInspection: true,
        });
    } else {
        res.json({
            message: "already visited",
        });
    }
});

app.get("/feedback", (req, res) => {
    if (components.includes("Feedback")){
        res.render("customerfeedback.ejs", {
            cssFiles: ["css/header.css", "css/customerfeedback.css", "css/footer.css"],
            runningInspection: true,
        });
    } else{
        res.json({
            message: "already visited",
        });
    }
});

app.post("/postHeader", async (req, res) => {
    let headerContent = {};
    components = components.filter((component) => (component != "Header"));
    headerContent.truck_serial_number = req.body.serial_num;
    headerContent.truck_model = req.body.model_num;
    try {
        const response = (await axios({
            method: "get",
            baseURL: apiURL,
            url: "inspectionID",
            responseType: "json",
        })).data;
        headerContent.inspection_id = parseInt(response.count) + 1;
    } catch (error) {
        console.log(error);
    }
    headerContent.inspector_name = "Inspector Name";//fetch from caterpillar database
    headerContent.inspection_employee_id = "Employee ID";//fetch from caterpillar database
    headerContent.date_time = new Date();
    headerContent.location = req.body.inspection_loc;
    if (req.body.geo_coordinates != "") {
        headerContent.geo_coordinates = req.body.geo_coordinates;
    } else{
        headerContent.geo_coordinates = "N/A";
    }
    headerContent.service_meter_hours = req.body.odo_reading;
    headerContent.inspector_signature = "e-signature";//fetch from caterpillar database
    headerContent.cat_customer_id = req.body.cust_id;
    headerContent.customer_name = "Customer Name";//fetch from caterpillar database using customer id
    currentInspection.header = headerContent;
    res.redirect("/componentChoice");
});

app.post("/sendReport", async (req, res) => {
    const componentName = req.body.component_name;
    components = components.filter((component) => (component != componentName));
    let componentContent = {};
    if (componentName === "Tires"){
        componentContent.left_front_pressure = req.body.question1 + "psi";
        componentContent.right_front_pressure = req.body.question2 + "psi";
        componentContent.left_front_condition = req.body.question3;
        componentContent.right_front_condition = req.body.question4;
        componentContent.left_rear_pressure = req.body.question5 + "psi";
        componentContent.right_rear_pressure = req.body.question6 + "psi";
        componentContent.left_rear_condition = req.body.question7;
        componentContent.right_rear_condition = req.body.question8;
        currentInspection.tires = componentContent;
    } else if(componentName === "Battery"){
        componentContent.make = req.body.question1;
        componentContent.replacement_date = req.body.question2;
        componentContent.voltage = req.body.question3 + "V";
        componentContent.water_level = req.body.question4;
        componentContent.condition_dammage = req.body.question5;
        componentContent.leak_rust = req.body.question6;
        currentInspection.battery = componentContent;
    } else if(componentName === "Exterior"){
        componentContent.rust_dent_damage = req.body.question1;
        componentContent.oil_leak_suspension = req.body.question2;
        currentInspection.exterior = componentContent;
    } else if(componentName === "Brakes"){
        componentContent.fluid_level = req.body.question1;
        componentContent.front_condition = req.body.question2;
        componentContent.rear_condition = req.body.question3;
        componentContent.emergency_brake = req.body.question4;
        currentInspection.brakes = componentContent;
    } else if(componentName === "Engine"){
        componentContent.rust_dent_damage = req.body.question1;
        componentContent.oil_condition = req.body.question2;
        componentContent.oil_color = req.body.question3;
        componentContent.brake_fluid_condition = req.body.question4;
        componentContent.brake_fluid_color = req.body.question5;
        componentContent.oil_leak = req.body.question6;
        currentInspection.engine = componentContent;
    }
    const response = (await axios({
        method: "post",
        baseURL: apiURL,
        url: "getSummary",
        data: {
            content: JSON.stringify(componentContent),
        },
        responseType: "json",
    })).data;
    summaryList[componentName] = response.content;
    res.render("componentSummary.ejs", {
        cssFiles: ["css/header.css", "css/componentSummary.css", "css/footer.css"],
        runningInspection: true,
        component: componentName,
        summary: summaryList[componentName],
    });
});

app.post("updateSummary", (req, res) =>{
    summaryList[req.body.component] = req.body.summary;
    res.redirect("/componentChoice");
});

app.post("/feedback", async (req, res) =>{
    console.log("sent feedback");
    let feedbackContent = {};
    components = components.filter((component) => (component != "Feedback"));
    feedbackContent.feedback = req.body.feedback;
    currentInspection.customer_feedback = feedbackContent;
    console.log(currentInspection);
    try {
        const response = (await axios({
            method: "post",
            baseURL: apiURL,
            url: "addInspection",
            data: {
                inspection: JSON.stringify(currentInspection),
            }
        })).data;
        console.log(response);
    } catch (error) {
        console.log(error);
    }
    try {
        const response = (await axios({
            method: "post",
            baseURL: apiURL,
            url: "generateReport",
            data: {
                inspectionSummary: JSON.stringify(currentInspection),
            }
        })).data;
        console.log(response.content);
    } catch (error) {
        console.log(error);
    }
    res.redirect("/");
});