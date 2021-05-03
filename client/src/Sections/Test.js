import React from 'react';
import { Paper, Card, CardContent, List, ListItem, Typography, makeStyles } from '@material-ui/core'
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
    }
  }));

const ArticleCard = ({ title, pubDate, sourceID }) => {
    const classes = useStyles();
    return (
        <Card variant="outlined" className={classes.card}>
            <CardContent className={classes.cardContent}>
                <Typography variant="h6" style={{fontSize: "18px"}}>
                    {title}
                </Typography>
                <Typography variant="body1">
                    {pubDate}
                </Typography>
            </CardContent>
        </Card>
    )
};

const Column = ({ source, id, data, select }) => {
    const classes = useStyles();
    const handler = (index, id) =>{
      console.log(index) 
      console.log(id) 
    };
    return (
        <Paper classes={{root: classes.paperRoot}} elevation={3} >
            {data? <List className={classes.list}>
                {data.map((article, index) => (
                    <ListItem key={index} className={classes.listItem} onClick={() => select(id, index)}>
                        <ArticleCard title={article.title} pubDate={article.pubDate} sourceID={id}/>
                    </ListItem>
                ))}
            </List> : <Typography variant="h5" style={{textAlign: "center", marginTop: "20px"}}>No Matches</Typography>}
        </Paper>
    )
};


export const TestView = ({ data, selectArticle }) => {
    return (
        <div style={{display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", 
                    gridTemplateRows: "1fr", 
                    gap: "100px", 
                    justifyContent: "center",
                    padding: "50px"}}>
            <Column source="BBC News" id="0" data={data.bbc_news} select={selectArticle} />
            <Column source="The Guardian" id="1" data={data.the_guardian} select={selectArticle}/>
            <Column source="Sky News" id="2" data={data.sky_news} select={selectArticle}/>
            <Column source="Daily Mail" id="3" data={data.daily_mail} select={selectArticle}/>
        </div>
    ); 
  };

export default TestView
