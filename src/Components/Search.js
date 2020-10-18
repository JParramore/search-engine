import React, { useState} from 'react';
import 'antd/dist/antd.css';
import '../index.css';
import { Input, List, } from 'antd';

const Search = () => {
    const [results, setResults] = useState([])
    const { Search } = Input;

    const handleInputChange = (e) => {
        const keyWords = e.target.value

        fetch(`/search?${new URLSearchParams({ q: keyWords })}`).then(response =>
            response.json())
            .then(data => {
                setResults(data)
            })
    }

    return <div><Search
        placeholder="input search text"
        onSearch={value => console.log(value)}
        onChange={handleInputChange}
        enterButton />
        <List
            itemLayout="vertical"
            size="small"
            locale={{ emptyText: '...' }}
            pagination={{
                onChange: page => {
                    console.log(page);
                },
                pageSize: 10,
            }}
            dataSource={results}
            footer={
                <div>
                    <b>Search engine</b> footer text
      </div>
            }
            renderItem={result => (
                <List.Item
                    key={result.url}
                >
                    <List.Item.Meta
                        title={<a href={result.url}>{result.title}</a>}
                        description={result.url}
                    />
                    {result.description}
                </List.Item>
            )}
        />
    </div>
}

export default Search;