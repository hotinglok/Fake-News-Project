import React, { useState } from "react";
import { DragDropContext, Draggable, Droppable } from "react-beautiful-dnd";
import { Box, CardActionArea, List, ListItem, Paper, Typography, makeStyles } from '@material-ui/core';
import { v4 as uuid } from 'uuid';

const useStyles = makeStyles(theme => ({
  header: {
    padding: "20px",
    display: "flex",
    flexDirection: "column",
    maxWidth: "40vW",
  },
  keyword_container: {
    display: "grid",
    gridTemplateRows: "1fr 1fr 1fr",
    gridTemplateColumns: "1fr 1fr 1fr",
    gap: "1rem"
  },
  keyword: {
    display: "flex",
    flexDirection: "row",
    justifyContent: "space-between",
    height: "1.5rem",
    width: "100%",
    padding: "1rem",
    backgroundColor: "#F0FFFA"
  },
  card: {
      display: "flex",
      flexDirection: "column",
      justifyContent: "space-between",
      userSelect: "none",
      fontSize: "14px",
      color: "#212121",
      padding: 16,
      border: "2px",
      borderRadius: "12px",
      margin: "0 0 12px 0",
      minHeight: "12rem",
      backgroundColor: "#ffffff",
      transition: "background 0.2s",
      '&:active': {
        backgroundColor: '#fff9c4'
      }
  },
  droppable: {
    backgroundColor: "#eceff1",
    padding: "10px 10px 2px 10px",
    border: "1px",
    borderRadius: "12px",
    width: "40rem",
    minHeight: "10.2rem",
  },
  high: {
    color: "#00e676",
    fontSize: "1rem"
  },
  medium: {
    color: "#ffb300",
    fontSize: "1rem"
  },
  low: {
    color: "#d32f2f",
    fontSize: "1rem"
  }
}));

const AddUUID = (data) => {
  const test = data
  const result = []
  for(var i in test){
    test[i].id = uuid();
    result.push(test[i])
  }
  return(result)
}

const getStyle = (style) => {
  if (style?.transform) {
    const axisLockY = `translate(0px, ${style.transform.split(',').pop()}`;
    return {
      ...style,
      transform: axisLockY,
    };
  }
  return style;
}

const openInNewTab = (url) => {
  const newWindow = window.open(url, '_blank', 'noopener,noreferrer')
  if (newWindow) newWindow.opener = null
}

const Header = ({ data }) => {
  const classes = useStyles();
  const date_published = new Date(data.date_published).toLocaleString()
  const date_modified = new Date(data.date_modified).toLocaleString()
  return(
      <Box style={{padding: "1rem"}} onClick={() => openInNewTab(data.url)}>
        <CardActionArea>
          <Paper elevation={2} className={classes.header}>
              <Typography variant="h3" style={{textAlign: "center", marginBottom: "1rem"}}>
                {data.source}
              </Typography>
              <Typography variant="h4" style={{marginBottom: "1rem"}}>
                {data.headline}
              </Typography>
              <Typography variant="h6" style={{marginBottom: "1rem", fontSize: "1.2rem", }}>
                Date Published: {date_published}
              </Typography>
              <Typography variant="h6" style={{marginBottom: "1rem", fontSize: "1.2rem"}}>
                Last Modified: {date_modified}
              </Typography>
              <Typography variant="h6" style={{marginBottom: "1rem", fontSize: "1.2rem"}}>
                Total Sentences: {data.num_sentences}
              </Typography>
              <Typography variant="h6" style={{marginBottom: "0.5rem", fontSize: "1.15rem"}}>
                Keywords:
              </Typography>
              <KeyWords data={data.keywords}/>
          </Paper>
        </CardActionArea>
      </Box>
  )

}

const KeyWords = ({ data }) =>{
  const classes = useStyles();
  return(
    <List className={classes.keyword_container} variant="outlined" elevation={0} >
      {data.map((keyword) => (
        <ListItem key={uuid()}>
          <Paper className={classes.keyword} variant="outlined" elevation={3}>
            <Typography variant="body1" style={{fontWeight: "bold"}}>
              {keyword.keyword}
            </Typography>
            <Typography variant="body1">
              {keyword.frequency}
            </Typography>
          </Paper>
        </ListItem>
      ))}
    </List>
  )
}

const onDragEnd = (result, columns, setColumns) => {
  if (!result.destination) return;
  const { source, destination } = result;

  if (source.droppableId !== destination.droppableId) {
    const sourceColumn = columns[source.droppableId];
    const destColumn = columns[destination.droppableId];
    const sourceItems = [...sourceColumn.items];
    const destItems = [...destColumn.items];
    const [removed] = sourceItems.splice(source.index, 1);
    destItems.splice(destination.index, 0, removed);
    setColumns({
      ...columns,
      [source.droppableId]: {
        ...sourceColumn,
        items: sourceItems
      },
      [destination.droppableId]: {
        ...destColumn,
        items: destItems
      }
    });
    } else {
      const column = columns[source.droppableId];
      const copiedItems = [...column.items];
      const [removed] = copiedItems.splice(source.index, 1);
      copiedItems.splice(destination.index, 0, removed);
      setColumns({
        ...columns,
        [source.droppableId]: {
          ...column,
          items: copiedItems
        }
      });
  }
};

export const AnalysisView = ({ data }) => {
  const columnsFromAPI = {
    [uuid()]: {
      name: "Sorted Quotations",
      items: AddUUID(data.first_source.sorted_quotations)
    },
    [uuid()]: {
      name: "Sorted Quotations",
      items: AddUUID(data.second_source.sorted_quotations)
    },
    [uuid()]: {
      name: "Unsorted Quotations",
      items: AddUUID(data.first_source.unsorted_quotations)
    },
    [uuid()]: {
      name: "Unsorted Quotations",
      items: AddUUID(data.second_source.unsorted_quotations)
    },
    [uuid()]: {
      name: "Sorted Stats",
      items: AddUUID(data.first_source.sorted_stats)
    },
    [uuid()]: {
      name: "Sorted Stats",
      items: AddUUID(data.second_source.sorted_stats)
    },
    [uuid()]: {
      name: "Unsorted Stats",
      items: AddUUID(data.first_source.unsorted_stats)
    },
    [uuid()]: {
      name: "Unsorted Stats",
      items: AddUUID(data.second_source.unsorted_stats)
    },
    [uuid()]: {
      name: "Sorted Text",
      items: AddUUID(data.first_source.sorted_text)
    },
    [uuid()]: {
      name: "Sorted Text",
      items: AddUUID(data.second_source.sorted_stats)
    },
    [uuid()]: {
      name: "Unsorted Text",
      items: AddUUID(data.first_source.unsorted_text)
    },
    [uuid()]: {
      name: "Unsorted Text",
      items: AddUUID(data.second_source.unsorted_text)
    },
    [uuid()]: {
      name: "Irrelevant",
      items: []
    },
    [uuid()]: {
      name: "Irrelevant",
      items: []
    }
  };
  const [columns, setColumns] = useState(columnsFromAPI);
  const classes = useStyles();
  return (
    <div style={{ display: "grid", 
                  gridTemplateColumns: "1fr 1fr",
                  justifyContent: "center", 
                  height: "100%",
                  padding: "3rem 0 3rem 0" }}>
      <Header data={data.first_source}/>
      <Header data={data.second_source}/>
      <DragDropContext
        onDragEnd={result => onDragEnd(result, columns, setColumns)}
      >
        {Object.entries(columns).map(([columnId, column]) => {
          return (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                height: "100%",
              }}
              key={columnId}
            >
              <Typography variant="h4" component="h2" style={{paddingBottom: "1rem"}}>{column.name}</Typography>
              <div >
                <Droppable droppableId={columnId} key={columnId}>
                  {(provided, snapshot) => {
                    return (
                      <Paper
                        {...provided.droppableProps}
                        ref={provided.innerRef}
                        style={{
                          marginBottom: "2rem",
                          background: snapshot.isDraggingOver
                            ? "lightblue"
                            : "#eceff1"
                        }}
                        elevation={3}
                        className={classes.droppable}
                      >
                        {column.items.map((item, index) => {
                          return (
                            <Draggable
                              key={item.id}
                              draggableId={item.id}
                              index={index}
                            >
                              {(provided, snapshot) => {
                                return (
                                  <Paper
                                    elevation={3}
                                    ref={provided.innerRef}
                                    {...provided.draggableProps}
                                    {...provided.dragHandleProps}
                                    className={classes.card}
                                    style={getStyle(provided.draggableProps.style, snapshot)}
                                  >
                                    <Typography variant="body1" style={{fontSize: "1.0625rem"}}>
                                      {item.sentence}
                                    </Typography>
                                    <div style={{ display: "flex", flexDirection: "row", justifyContent: "space-between"}}>
                                      {item.score ? 
                                      <Typography variant="body2" className={item.score > 0.5 ? (item.score > 0.7 ? classes.high : classes.medium) : classes.low}>
                                        {item.score}
                                      </Typography> : <div> </div>}
                                      <Typography variant="body2" style={{fontSize: "1rem"}}>
                                        {item.index}
                                      </Typography>
                                    </div>
                                  </Paper>
                                );
                              }}
                            </Draggable>
                          );
                        })}
                        {provided.placeholder}
                      </Paper>
                    );
                  }}
                </Droppable>
              </div>
            </div>
          );
        })}
      </DragDropContext>
    </div>
  );
}

export default AnalysisView;
