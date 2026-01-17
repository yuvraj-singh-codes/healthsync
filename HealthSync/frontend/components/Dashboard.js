import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [healthData, setHealthData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchHealthData = async () => {
            try {
                const response = await axios.get('/api/health-data');
                setHealthData(response.data);
            } catch (err) {
                setError('Failed to fetch health data');
            } finally {
                setLoading(false);
            }
        };

        fetchHealthData();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard">
            <h1>User Health Dashboard</h1>
            <div className="health-data">
                {healthData.length > 0 ? (
                    healthData.map((data, index) => (
                        <div key={index} className="health-item">
                            <h2>{data.title}</h2>
                            <p>{data.description}</p>
                            <p>Date: {new Date(data.date).toLocaleDateString()}</p>
                        </div>
                    ))
                ) : (
                    <p>No health data available.</p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;