import React, { useState } from "react";
import { DragDropContext, Draggable, Droppable } from "react-beautiful-dnd";
import { Paper, Typography, makeStyles } from '@material-ui/core';
import { v4 as uuid } from 'uuid';
import DummyAnalysis from '../Dummy/AnalysisResults'

const useStyles = makeStyles(theme => ({
  paper: {
      userSelect: "none",
      fontSize: "14px",
      color: "#212121",
      padding: 16,
      border: "2px",
      borderRadius: "12px",
      margin: "0 0 12px 0",
      minHeight: "8rem",
      backgroundColor: "#ffffff",
      transition: "background 0.2s",
      '&:active': {
        backgroundColor: '#fff9c4'
    }
  }
}));

function AddUUID(data){
  const test = data
  const result = []
  for(var i in test){
    test[i].id = uuid();
    result.push(test[i])
  }
  return(result)
}

function getStyle(style) {
  if (style?.transform) {
    const axisLockY = `translate(0px, ${style.transform.split(',').pop()}`;
    return {
      ...style,
      transform: axisLockY,
    };
  }
  return style;
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
                  gridGap: "3rem",
                  justifyContent: "center", 
                  height: "100%" }}>
      <DragDropContext
        onDragEnd={result => onDragEnd(result, columns, setColumns)}
      >
        {Object.entries(columns).map(([columnId, column], index) => {
          return (
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center"
              }}
              key={columnId}
            >
              <Typography variant="h4" component="h2" style={{paddingBottom: "5px"}}>{column.name}</Typography>
              <div >
                <Droppable droppableId={columnId} key={columnId}>
                  {(provided, snapshot) => {
                    return (
                      <div
                        {...provided.droppableProps}
                        ref={provided.innerRef}
                        style={{
                          background: snapshot.isDraggingOver
                            ? "lightblue"
                            : "lightgrey",
                          padding: "10px 10px 2px 10px",
                          border: "1px",
                          borderRadius: "12px",
                          width: "40rem",
                          minHeight: "10.2rem",
                        }}
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
                                    className={classes.paper}
                                    style={getStyle(provided.draggableProps.style, snapshot)}
                                  >
                                    {console.log(item)}
                                    {item.sentence}
                                  </Paper>
                                );
                              }}
                            </Draggable>
                          );
                        })}
                        {provided.placeholder}
                      </div>
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