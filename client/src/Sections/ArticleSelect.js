import React, { useState } from 'react';
import { Button, Paper, Card, CardContent, List, ListItem, Typography, makeStyles } from '@material-ui/core'
import { style } from '@material-ui/system'

export const textColor = style({
  prop: 'color',
  themeKey: 'palette',
});

export const bgcolor = style({
  prop: 'bgcolor',
  cssProperty: 'backgroundColor',
  themeKey: 'palette',
});

const useStyles = makeStyles(theme => ({
    root: {
        display: "flex",
        flexWrap: "wrap",
        "& > *": {
            margin: theme.spacing(1),
            width: theme.spacing(16),
            height: theme.spacing(16)
        }
    },
    paperRoot: {
        backgroundColor: "#eceff1",
        alignItems: "center",
        display: "flex",
        flexDirection: "column"
    },
    list: {
        position: 'relative',
        overflow: 'auto',
        maxHeight: "75vH",
    },
    listItem: {
        paddingLeft: "0",
        paddingRight: "0"
    },
    header: {
        textAlign: "center",
        padding: "15px",
        width: "92%"
    },
    card: {
        minWidth: "330px",
        height: "140px",
        margin: "5px",
        padding: "16px 16px 0px 16px",
        transition: "background 0.5s",
        '&:hover': {
            backgroundColor: '#b3e5fc',
        }
    },
    cardContent: {
        height: "90%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "0"
    },
    button: {
        width: "90%",
        height: "3rem"
    },
    scoreHigh: {
        color: "#00e676"
    },
    scoreLow: {
        color: "#d32f2f"
    },

  }));

const ArticleCard = ({ title, pubDate, score }) => {
    const classes = useStyles();
    return (
        <Card variant="outlined" className={classes.card}>
            <CardContent className={classes.cardContent}>
                <Typography variant="h6" style={{fontSize: "18px"}}>
                    {title}
                </Typography>
                {score ? <Typography variant="body1" className={score > 0.5? classes.scoreHigh : classes.scoreLow }>
                    {score}
                </Typography> : <></>}
                <Typography variant="body1">
                    {pubDate}
                </Typography>
            </CardContent>
        </Card>
    )
};

const Header = ({ source, matches }) => {
    const classes = useStyles();
    return (
        <Card variant="outlined" className={classes.header}>
            <CardContent>
                <Typography variant="h3" component="h2" style={{paddingBottom: "5px"}}>
                    {source}
                </Typography>
                {matches > 1? <Typography variant="h6" className={classes.pos} color="textSecondary">
                    Matches: {matches}
                </Typography> : <Typography variant="h6" className={classes.pos} color="textSecondary">
                    Root Article
                </Typography>}
            </CardContent>
        </Card>
    )
};  


const Column = ({ source, data, select, disabled, submit, link1, link2 }) => {
    const classes = useStyles();
    return (
        <Paper classes={{root: classes.paperRoot}} elevation={3} >
            <Header source={source} matches={data? Object.keys(data).length : "No Matches"} />
            {Object.keys(data).length > 1 ? 
                <List className={classes.list}>
                    {data.map((article, index) => (
                        <ListItem key={index} className={classes.listItem} onClick={() => select(article.link)} >
                            <ArticleCard title={article.title} pubDate={article.pubDate} score={article.score}/>
                        </ListItem>
                    ))}
                </List> :
                <> 
                    <List className={classes.list}>
                        {data.map((article, index) => (
                            <ListItem key={index} className={classes.listItem} onClick={() => select(article.link)}>
                                <ArticleCard title={article.title} pubDate={article.pubDate} score={article.score}/>
                            </ListItem>
                        ))}
                    </List>
                    <Button className={classes.button} variant="contained" color="primary" disabled={disabled} onClick={() => submit(link1, link2)}>
                        Analyse
                    </Button>
                </>}
        </Paper>
    )
};


export const ArticleSelectView = ({ data, searchData, submitLinks }) => {

    const [selected, setSelected] = useState(1);
    const [link1, setLink1] = useState('');
    const [link2, setLink2] = useState('');
    const [disabled, setDisabled] = useState(true)
    const selectItem = (link) =>{
        if(selected !== 2){
            setSelected(selected + 1)
        }
        if(selected === 1){
            setLink1(link);
        }
        else if(selected === 2){
            setLink2(link);
            setDisabled(false)
        }
    }
    return (
        <div style={{display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", 
                    gridTemplateRows: "1fr", 
                    gap: "100px", 
                    justifyContent: "center",
                    padding: "50px"}}>
            <Column source="BBC News" id="0" data={data.bbc_news} select={selectItem} disabled={disabled} link1={link1} link2={link2} submit={submitLinks} search={searchData} />
            <Column source="The Guardian" id="1" data={data.the_guardian} select={selectItem} disabled={disabled} link1={link1} link2={link2} submit={submitLinks} search={searchData}/>
            <Column source="Sky News" id="2" data={data.sky_news} select={selectItem} disabled={disabled} link1={link1} link2={link2} submit={submitLinks} search={searchData}/>
            <Column source="Daily Mail" id="3" data={data.daily_mail} select={selectItem} disabled={disabled} link1={link1} link2={link2} submit={submitLinks} search={searchData}/>
        </div>
    ); 
  };

export default ArticleSelectView
