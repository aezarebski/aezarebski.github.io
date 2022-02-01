const randomColour = () => {
    let colour = '#';
    for (let i = 0; i < 6; i++){
        const random = Math.random();
        const bit = (random * 16) | 0;
        colour += (bit).toString(16);
    };
    return colour;
};

const colourfulTable = () => {
    let table = '';
    table += '<table>';
    for (let i = 0; i < 10; i++) {
        table += '<tr>';
        for (let j = 0; j < 10; j++) {
            table += '<td>';
            table += `<p style='color: ${randomColour()};'>colour</p>`;
            table += '</td>';
        }
        table += '</tr>';
    }
    table += '</table>';
    return table;
};

const main = document.getElementById('main');
main.innerHTML = colourfulTable();
