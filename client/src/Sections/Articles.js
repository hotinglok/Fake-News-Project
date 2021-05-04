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
    },
    paperRoot: {
        backgroundColor: "#eceff1",
        alignItems: "center"
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
        padding: "15px"
    },
    card: {
        minWidth: "330px",
        height: "140px",
        margin: "5px",
        padding: "16px 16px 0px 16px",
        transition: "background 0.5s",
        '&:hover': {
            backgroundColor: '#b3e5fc',
        },
    },
    cardContent: {
        height: "90%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
        padding: "0"
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

const Header = ({ source, matches }) => {
    const classes = useStyles();
    return (
        <Card variant="outlined" className={classes.header}>
            <CardContent>
                <Typography variant="h3" component="h2" style={{paddingBottom: "5px"}}>
                    {source}
                </Typography>
                <Typography variant="h6" className={classes.pos} color="textSecondary">
                    Matches: {matches}
                </Typography>
            </CardContent>
        </Card>
    )
};  


const Column = ({ source, id, data, select, search }) => {
    const classes = useStyles();
    return (
        <Paper classes={{root: classes.paperRoot}} elevation={3} >
            <Header source={source} matches={data? Object.keys(data).length : "No Matches"} />
            {data? <List className={classes.list}>
                {data.map((article, index) => (
                    <ListItem key={index} className={classes.listItem} onClick={() => select(id, index, search.keywords, search.date, search.extra_days)}>
                        <ArticleCard title={article.title} pubDate={article.pubDate} sourceID={id} style={{width: "100%"}}/>
                    </ListItem>
                ))}
            </List> : <Typography variant="h5" style={{textAlign: "center", marginTop: "20px"}}>No Matches</Typography>}
        </Paper>
    )
};


export const ArticlesView = ({ data, searchData, selectArticle }) => {
    console.log(searchData)
    return (
        <div style={{display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", 
                    gridTemplateRows: "1fr", 
                    gap: "100px", 
                    justifyContent: "center",
                    padding: "50px"}}>
            <Column source="BBC News" id="0" data={data.bbc_news} select={selectArticle} search={searchData} />
            <Column source="The Guardian" id="1" data={data.the_guardian} select={selectArticle} search={searchData}/>
            <Column source="Sky News" id="2" data={data.sky_news} select={selectArticle} search={searchData}/>
            <Column source="Daily Mail" id="3" data={data.daily_mail} select={selectArticle} search={searchData}/>
        </div>
    ); 
  };

export default ArticlesView
