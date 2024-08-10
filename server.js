import express from "express";

const app = express();
const port = 4000;

class user{
    constructor(username, password){
        this.username = username;
        this.password = password;
    }
}

class inspection{
    static numberOFInspections = 1;
    constructor(user, serialno, modelno, location, pdfPath){
        this.id = this.numberOFInspections;
        this.username = user.username;
        this.serialno = serialno;
        this.modelno = modelno;
        this.location = location;
        this.dateAndTime = new Date();
        this.pdfPath = pdfPath;
        this.numberOFInspections++;
    }
}

app.listen(port, () =>{
    console.log("Server running on port " + port);
});

app.post("/login", (req, res) =>{

})