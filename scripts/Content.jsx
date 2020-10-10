    
import * as React from 'react';


import { Button } from './Button';
import { Socket } from './Socket';

export function Content() {
    const [items, setItems] = React.useState([]);
    
    function getNewItems() {
        React.useEffect(() => {
            Socket.on('Grocery list received', (data) => {
                console.log("Received grocery list from server: " + data['groceryList']); // TODO rework data fields
                setItems(data['groceryList']);
            })
        });
    }
    
    getNewItems();

    return (
        <div>
            <div id="messageSubmission">
                <Button />
            </div>
            <div id="messageHistory">
                <ul>
                    {items.map((item, index) =>
                        <li key={index}>{item}</li>)}
                </ul>
            </div>
        </div>
    );
}
