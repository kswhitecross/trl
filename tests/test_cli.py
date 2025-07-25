# Copyright 2020-2025 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
import sys
import tempfile
import unittest
from io import StringIO
from unittest.mock import patch

import yaml


@unittest.skipIf(
    sys.version_info < (3, 10),
    "Transformers' generation codebase uses a Python >3.10 syntax (`str | None`), which seems to cause the CLI tests "
    "to fail on Python <3.10.",  # let's say it's a known issue, but not expected to be fixed, because too niche
)
class TestCLI(unittest.TestCase):
    def test_dpo(self):
        from trl.cli import main

        with tempfile.TemporaryDirectory() as tmp_dir:  # Create a temporary directory
            command = f"trl dpo --output_dir {tmp_dir} --model_name_or_path trl-internal-testing/tiny-Qwen2ForCausalLM-2.5 --dataset_name trl-internal-testing/zen --dataset_config standard_preference --report_to none"
            with patch("sys.argv", command.split(" ")):
                main()

    def test_dpo_multiple_loss_types(self):
        from trl.cli import main

        with tempfile.TemporaryDirectory() as tmp_dir:
            command = f"trl dpo --output_dir {tmp_dir} --model_name_or_path trl-internal-testing/tiny-Qwen2ForCausalLM-2.5 --dataset_name trl-internal-testing/zen --dataset_config standard_preference --report_to none --loss_type sigmoid bco_pair --loss_weights 1.0 0.5"
            with patch("sys.argv", command.split(" ")):
                main()

    @patch("sys.stdout", new_callable=StringIO)
    def test_env(self, mock_stdout):
        from trl.cli import main

        command = "trl env"
        with patch("sys.argv", command.split(" ")):
            main()
        self.assertIn("TRL version: ", mock_stdout.getvalue().strip())

    def test_grpo(self):
        from trl.cli import main

        with tempfile.TemporaryDirectory() as tmp_dir:  # Create a temporary directory
            command = f"trl grpo --output_dir {tmp_dir} --model_name_or_path trl-internal-testing/tiny-Qwen2ForCausalLM-2.5 --reward_model_name_or_path trl-internal-testing/tiny-Qwen2ForSequenceClassification-2.5 --dataset_name trl-internal-testing/zen --dataset_config standard_prompt_only --num_generations 4 --max_completion_length 32 --report_to none"
            with patch("sys.argv", command.split(" ")):
                main()

    def test_kto(self):
        from trl.cli import main

        with tempfile.TemporaryDirectory() as tmp_dir:  # Create a temporary directory
            command = f"trl kto --output_dir {tmp_dir} --model_name_or_path trl-internal-testing/tiny-Qwen2ForCausalLM-2.5 --dataset_name trl-internal-testing/zen --dataset_config standard_unpaired_preference --report_to none"
            with patch("sys.argv", command.split(" ")):
                main()

    def test_sft(self):
        from trl.cli import main

        with tempfile.TemporaryDirectory() as tmp_dir:  # Create a temporary directory
            command = f"trl sft --output_dir {tmp_dir} --model_name_or_path trl-internal-testing/tiny-Qwen2ForCausalLM-2.5 --dataset_name trl-internal-testing/zen --dataset_config standard_language_modeling --report_to none"
            with patch("sys.argv", command.split(" ")):
                main()

    def test_sft_config_file(self):
        from trl.cli import main

        with tempfile.TemporaryDirectory() as tmp_dir:  # Create a temporary directory
            output_dir = os.path.join(tmp_dir, "output")

            # Create a temporary config file
            config_path = os.path.join(tmp_dir, "config.yaml")
            config_content = {
                "model_name_or_path": "trl-internal-testing/tiny-Qwen2ForCausalLM-2.5",
                "dataset_name": "trl-internal-testing/zen",
                "dataset_config": "standard_language_modeling",
                "report_to": "none",
                "output_dir": output_dir,
                "lr_scheduler_type": "cosine_with_restarts",
            }
            with open(config_path, "w") as config_file:
                yaml.dump(config_content, config_file)

            # Test the CLI with config file
            command = f"trl sft --config {config_path}"
            with patch("sys.argv", command.split(" ")):
                main()

            # Verify that output directory was created
            self.assertTrue(os.path.exists(output_dir))


if __name__ == "__main__":
    unittest.main()
