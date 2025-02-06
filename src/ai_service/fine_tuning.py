import logging
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments
from datasets import load_dataset
import torch

def fine_tune_model(model_id: str, dataset_name: str, output_dir: str, block_size: int = 128, batch_size: int = 16, num_epochs: int = 3):
    """
    Fine-tunes a pre-trained model for code generation.

    Args:
        model_id (str): The ID of the pre-trained model to fine-tune.
        dataset_name (str): The name of the dataset to use for fine-tuning.
        output_dir (str): The directory to save the fine-tuned model.
        block_size (int): The block size to use for the dataset.
        batch_size (int): The batch size to use for training.
        num_epochs (int): The number of epochs to train for.
    """
    logging.info(f"Fine-tuning model {model_id} with dataset {dataset_name}")

    try:
        # Load the dataset
        dataset = load_dataset(dataset_name, split="train")

        # Load the tokenizer and model
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)

        # Tokenize the dataset
        def tokenize_function(examples):
            return tokenizer(examples["text"])

        tokenized_dataset = dataset.map(tokenize_function, batched=True, num_proc=4, remove_columns=["text"])

        # Group the texts in blocks
        def group_texts(examples):
            # Concatenate all texts
            concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
            total_length = len(concatenated_examples[list(examples.keys())[0]])
            # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
            # customize this part to your needs.
            total_length = (total_length // block_size) * block_size
            # Split by chunks of max_len
            result = {
                k: [t[i : i + block_size] for i in range(0, total_length, block_size)]
                for k, t in concatenated_examples.items()
            }
            result["labels"] = result["input_ids"].copy()
            return result

        lm_dataset = tokenized_dataset.map(group_texts, batched=True, num_proc=4)

        # Define the training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            overwrite_output_dir=True,
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            save_steps=10_000,
            save_total_limit=2,
        )

        # Create the trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=lm_dataset,
        )

        # Train the model
        trainer.train()

        # Save the fine-tuned model
        trainer.save_model(output_dir)

        logging.info(f"Fine-tuning complete. Model saved to {output_dir}")

    except Exception as e:
        logging.error(f"Error during fine-tuning: {e}", exc_info=True)
        raise
