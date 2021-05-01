import React, { useState } from "react";
import { DragDropContext, Draggable, Droppable } from "react-beautiful-dnd";
import { v4 as uuid } from 'uuid';

const itemsFromBackend = [
  { id: uuid(), content: "First task" },
  { id: uuid(), content: "Second task" },
  { id: uuid(), content: "Third task" },
  { id: uuid(), content: "Fourth task" },
  { id: uuid(), content: "The Duke of Edinburgh's link to the Navy and love of the sea will be a focus at the Windsor service." },
  { id: uuid(), content: "Fifth task" },
  { id: uuid(), content: "Fifth task" },
  { id: uuid(), content: "Fifth task" },
  { id: uuid(), content: "Fifth task" },
  { id: uuid(), content: "Fifth task" },
];

const columnsFromBackend = {
  [uuid()]: {
    name: "Headlines",
    items: itemsFromBackend
  },
  [uuid()]: {
    name: "Headlines",
    items: []
  },
  [uuid()]: {
    name: "Keywords",
    items: []
  },
  [uuid()]: {
    name: "Keywords",
    items: []
  },
  [uuid()]: {
    name: "Sorted Quotations",
    items: []
  },
  [uuid()]: {
    name: "Sorted Quotations",
    items: []
  },
  [uuid()]: {
    name: "Unsorted Quotations",
    items: []
  },
  [uuid()]: {
    name: "Unsorted Quotations",
    items: []
  },
  [uuid()]: {
    name: "Sorted Stats",
    items: []
  },
  [uuid()]: {
    name: "Sorted Stats",
    items: []
  },
  [uuid()]: {
    name: "Unsorted Stats",
    items: []
  },
  [uuid()]: {
    name: "Unsorted Stats",
    items: []
  },
  [uuid()]: {
    name: "Sorted Text",
    items: []
  },
  [uuid()]: {
    name: "Sorted Text",
    items: []
  },
  [uuid()]: {
    name: "Unsorted Text",
    items: []
  },
  [uuid()]: {
    name: "Unsorted Text",
    items: []
  },
  [uuid()]: {
    name: "Irrelevant",
    items: []
  }
};

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

function AnalysisView() {
  const [columns, setColumns] = useState(columnsFromBackend);
  return (
    <div style={{ display: "grid", 
                  gridTemplateColumns: "240px 240px",
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
              <h2>{column.name}</h2>
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
                          padding: 4,
                          width: 250,
                          minHeight: 500
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
                                  <div
                                    ref={provided.innerRef}
                                    {...provided.draggableProps}
                                    {...provided.dragHandleProps}
                                    style={{
                                      userSelect: "none",
                                      fontSize: "12px",
                                      padding: 16,
                                      margin: "0 0 8px 0",
                                      minHeight: "50px",
                                      backgroundColor: snapshot.isDragging
                                        ? "#263B4A"
                                        : "#456C86",
                                      color: "white",
                                      ...provided.draggableProps.style
                                    }}
                                  >
                                    {item.content}
                                  </div>
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
