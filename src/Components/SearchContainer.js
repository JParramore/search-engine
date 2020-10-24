import React, { useState } from 'react';
import 'antd/dist/antd.css';
import '../index.css';
import { Input, List, Typography } from 'antd';
const { Text } = Typography;

const SearchContainer = () => {
    const [data, setData] = useState([])

    const { Search } = Input

    const handleInputChange = (e) => {
        const keyWords = e.target.value
        fetch(`/search?${new URLSearchParams({ q: keyWords })}`).then(response =>
            response.json())
            .then(data => {
                setData(data)
            })
    }

    return <div><Search
        className="search-box"
        placeholder="Search over 200 technical blogs"
        onChange={handleInputChange}
        enterButton
        size="large" />
        <Text type="secondary">{data.stats}</Text>
        <List
            className="res-list"
            itemLayout="vertical"
            size="small"
            locale={{ emptyText: ' ' }}
            pagination={{
                simple: true,
                pageSize: 10,
                hideOnSinglePage: true
            }}
            dataSource={data.results}
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

export default SearchContainer;