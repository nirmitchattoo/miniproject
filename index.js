const express = require('express');
const axios = require('axios');
const app = express();
const languageWords = require("./data.json")
const mainData = languageWords['en'].concat(languageWords['hi'])

let data = []
for(let i=0; i<mainData.length; i++){
    data.push((mainData[i]+" ").toLowerCase());
    data.push((" "+mainData[i]).toLowerCase())
}

data.sort();
data.reverse();

app.use(express.json());

app.post('/check-filter', async(req, res)=>{
    let body = req.body;
    let text = body['text'].toLowerCase();
    let abusiveWords = [];
    data.forEach(ele => {
        if(text.split(ele).length > 1)
        {
            abusiveWords.push(ele.trim());
            let abuseStarred = "";
            for(let i=0; i<ele.length; i++){
                // if(i==0 || i==ele.length-1){
                //     abuseStarred+=ele[i]
                // }
                // abuseStarred += "*";
            }
            text = text.replaceAll(ele, abuseStarred)
        }
    });
    let set = new Set(abusiveWords);
    abusiveWords = [...set]
    if(abusiveWords.length==0)
    {
        return res.status(201).json({
            message: "No Abusive Words Found!",
            data: abusiveWords
        });
    }else{
        return res.status(201).json({
            message: "Abusive Words Found!",
            data: abusiveWords,
            removedAbusedWords: text
        });
    }
});

app.post('/check-filter-url', async(req, res)=>{
    let body = req.body;
    let url = body['url'];
    let abusiveWords = [];
    let text = await axios.get(url)
    text = text["data"]
    data.forEach(ele => {
        if(text.split(ele).length > 1)
        {
            abusiveWords.push(ele.trim());
            let abuseStarred = "";
            for(let i=0; i<ele.length; i++){
                if(i==0 || i==ele.length-1){
                    abuseStarred+=ele[i]
                }
                abuseStarred += "*";
            }
            text = text.replaceAll(ele, abuseStarred)
        }
    });
    let set = new Set(abusiveWords);
    abusiveWords = [...set]
    if(abusiveWords.length==0)
    {
        return res.status(201).json({
            message: "No Abusive Words Found!",
            data: abusiveWords
        });
    }else{
        return res.status(201).json({
            message: "Abusive Words Found!",
            data: abusiveWords,
            removedAbusedWords: text
        });
    }
});

app.listen(5000, ()=>{
    console.log("Server Started!")
})