import React, { useState, useEffect } from 'react';
import { Select, Option, Button, Typography, Progress } from "@material-tailwind/react";
import axios from 'axios';

interface ModelSelectionProps {
    onStrategyChange: (strategy: string) => void;
    onModelChange: (model: string) => void;
    currentModel: string;
    strategy: string;
}

const ModelSelection: React.FC<ModelSelectionProps> = ({ onStrategyChange, onModelChange, currentModel: propCurrentModel, strategy: propStrategy }) => {
    const [selectedStrategy, setSelectedStrategy] = useState(propStrategy || 'auto');
    const [selectedModel, setSelectedModel] = useState('');
    const [isManual, setIsManual] = useState(propStrategy === 'manual');
    const [availableModels, setAvailableModels] = useState<string[]>([]);
    const [modelMappings, setModelMappings] = useState<{ [key: string]: string }>({});
    const [currentModel, setCurrentModel] = useState(propCurrentModel || '');
    const [updateButtonLoading, setUpdateButtonLoading] = useState(false);
    const [updateStatus, setUpdateStatus] = useState<string | null>(null);
    const [updateProgress, setUpdateProgress] = useState<number>(0); // 0 to 100
    const [sseError, setSseError] = useState<string | null>(null);

    useEffect(() => {
        setIsManual(selectedStrategy === 'manual');
        onStrategyChange(selectedStrategy);
    }, [selectedStrategy, onStrategyChange]);

    useEffect(() => {
        onModelChange(selectedModel);
    }, [selectedModel, onModelChange]);

    useEffect(() => {
        // Fetch initial settings from the backend
        axios.get('http://localhost:8000/settings')
            .then(response => {
                const { strategy, model } = response.data;
                setSelectedStrategy(strategy || 'auto');
                setSelectedModel(model || '');
                setIsManual(strategy === 'manual');
                setCurrentModel(model || '');
                onStrategyChange(strategy || 'auto');
                onModelChange(model || '');
            })
            .catch(error => {
                console.error("Error fetching settings:", error);
                setUpdateStatus("Error fetching settings.");
            });

        // Fetch available models from the backend
        axios.get('http://localhost:8000/models')
            .then(response => {
                setAvailableModels(response.data);
            })
            .catch(error => {
                console.error("Error fetching available models:", error);
                setUpdateStatus("Error fetching available models.");
            });

        // Fetch model name mappings from the backend
        axios.get('http://localhost:8000/model_mappings')
            .then(response => {
                setModelMappings(response.data);
            })
            .catch(error => {
                console.error("Error fetching model mappings:", error);
                setUpdateStatus("Error fetching model mappings.");
            });
    }, [onStrategyChange, onModelChange]);

    const handleStrategyChange = (value: string) => {
        setSelectedStrategy(value);
        axios.post('http://localhost:8000/set_strategy', { strategy: value })
            .then(response => {
                console.log(response.data.message);
                setIsManual(value === 'manual');
                onStrategyChange(value);
                setUpdateStatus(response.data.message);
            })
            .catch(error => {
                console.error("Error setting strategy:", error);
                setUpdateStatus("Error setting strategy.");
            });
        setSelectedModel(''); // Reset selected model when strategy changes
        onModelChange('');
        setCurrentModel('');
    };

    const handleModelChange = (value: string) => {
        setSelectedModel(value);
        axios.post('http://localhost:8000/set_model', { model: value })
            .then(response => {
                console.log(response.data.message);
                onModelChange(value);
                setCurrentModel(value);
                setUpdateStatus(response.data.message);
            })
            .catch(error => {
                console.error("Error setting model:", error);
                setUpdateStatus("Error setting model.");
            });
    };

    const handleUpdateModel = () => {
        setUpdateButtonLoading(true);
        setUpdateStatus("Updating model...");
        setUpdateProgress(0);
        setSseError(null);

        const eventSource = new EventSource('http://localhost:8000/update_model');

        eventSource.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                setUpdateProgress(data.progress);
                setUpdateStatus(data.message);
                setSseError(null);
            } catch (error) {
                console.error("Error parsing SSE data:", error);
                setUpdateStatus("Error parsing update data.");
                setSseError("Error parsing update data.");
                eventSource.close();
            }
        };

        eventSource.onerror = (error) => {
            console.error("SSE error:", error);
            setUpdateStatus("Error updating model. Check console for details.");
            setSseError("Error updating model. Check console for details.");
            setUpdateButtonLoading(false);
            eventSource.close();
        };

        eventSource.onclose = () => {
            console.log("SSE connection closed.");
            setUpdateButtonLoading(false);
            if (!sseError && updateProgress < 100) {
                setUpdateStatus("Update process completed, but progress may not be complete.");
            }
        };
    };

    return (
        <div>
            <div className="mb-4">
                <label htmlFor="strategy" className="block text-sm font-medium text-gray-700">
                    Model Selection Strategy:
                </label>
                <Select
                    id="strategy"
                    value={selectedStrategy}
                    onChange={handleStrategyChange}
                    label="Select Model Selection Strategy"
                >
                    <Option value="auto">Auto (Recommended)</Option>
                    <Option value="manual">Manual</Option>
                </Select>
            </div>

            {isManual && (
                <div className="mb-4">
                    <label htmlFor="model" className="block text-sm font-medium text-gray-700">
                        Current Model:
                    </label>
                    <Select
                        id="model"
                        value={selectedModel}
                        onChange={handleModelChange}
                        disabled={!isManual}
                        label="Select Model"
                    >
                        {availableModels.map((model) => (
                            <Option key={model} value={model}>
                                {model} ({modelMappings[model]})
                            </Option>
                        ))}
                    </Select>
                </div>
            )}

            {!isManual && (
                <div className="mb-4">
                    <label htmlFor="currentModel" className="block text-sm font-medium text-gray-700">
                        Current Model (Auto Selected):
                    </label>
                    <input
                        type="text"
                        id="currentModel"
                        className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md"
                        value={currentModel}
                        disabled
                    />
                </div>
            )}

            <Button variant="gradient" color="blue" onClick={handleUpdateModel} disabled={updateButtonLoading}>
                {updateButtonLoading ? "Updating..." : "Update Model"}
            </Button>

            {updateStatus && (
                <div className="mt-4">
                    <Typography variant="small" color={sseError ? "red" : "green"}>
                        {updateStatus}
                    </Typography>
                </div>
            )}

            {updateButtonLoading && (
                <div className="mt-4">
                    <Progress value={updateProgress} color="blue" />
                </div>
            )}
        </div>
    );
};

export default ModelSelection;
