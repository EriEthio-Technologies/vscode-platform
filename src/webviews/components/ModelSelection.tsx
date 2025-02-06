import React, { useState, useEffect } from 'react';
import { Select, Option } from "@material-tailwind/react";
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
            });

        // Fetch available models from the backend
        axios.get('http://localhost:8000/models')
            .then(response => {
                setAvailableModels(response.data);
            })
            .catch(error => {
                console.error("Error fetching available models:", error);
            });

        // Fetch model name mappings from the backend
        axios.get('http://localhost:8000/model_mappings')
            .then(response => {
                setModelMappings(response.data);
            })
            .catch(error => {
                console.error("Error fetching model mappings:", error);
            });
    }, [onStrategyChange, onModelChange]);

    const handleStrategyChange = (value: string) => {
        setSelectedStrategy(value);
        axios.post('http://localhost:8000/set_strategy', { strategy: value })
            .then(response => {
                console.log(response.data.message);
                setIsManual(value === 'manual');
                onStrategyChange(value);
            })
            .catch(error => {
                console.error("Error setting strategy:", error);
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
            })
            .catch(error => {
                console.error("Error setting model:", error);
            });
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
        </div>
    );
};

export default ModelSelection;
