import { useState } from 'react';
import axios from "axios";
import './App.css';

function App() {
  const mapper = [{"name":"","description":""}];
  const [jsonData, setjsonData] = useState(mapper)
  const [nameTemp, setnameTemp] = useState('')
  const [descTemp, setdescTemp] = useState('')

  function getData(){
	axios({
		method: "GET",
		url: "/widgets"
	})
	.then(res => {
		setjsonData(res.data)
	}).catch((error) => {
		if(error.response){
			console.log(error.response)
			console.log(error.response.status)
			console.log(error.response.headers)
		}
})}
  function clearDB(){
	axios({
		method: "GET",
		url: "/cleardb"
	})
  }
  function sendData(){
	const val = {'name': nameTemp, 'description': descTemp}
	console.log(val)
	axios({
		method: "POST",
		url: "/acceptData",
		data: val
	})
	
  }
  function handleSubmit(){
	sendData()
  }
  function handleNameChange(event){
	setnameTemp(event.target.value);
  }
  function handleDescChange(event){
	setdescTemp(event.target.value);
  }

  return (
    <div className="App">
      <header className="App-header">
	<p>To get your database details: </p>
	<button onClick={getData}>Click me!</button>
	<table>
		<th>Name</th><th>Description</th>
		{jsonData.map((item) => (
			<tr key ={item.name}>
				{Object.values(item).map((val) => (
					<td>&nbsp;&nbsp;{val}&nbsp;&nbsp;</td>
				))}
			</tr>
		))
		}	
	</table>
	<button onClick={clearDB}>Clear DB</button>
	<p>To add values to the database: </p>

	<form name="getinfo" method='POST'>
	<label>Name:
	<textarea
        type="text"
        id="name"
        name="name"
		cols="25"
        onChange={handleNameChange}

    /><br/></label>
	<label>Description:	
	<textarea
		name = 'desc'
		rows="2"
		cols="25"
		onChange={handleDescChange}
	/><br/></label>
	</form>
	<button onClick={handleSubmit}>Submit</button>
	</header>
	</div>
  );
}

export default App;
