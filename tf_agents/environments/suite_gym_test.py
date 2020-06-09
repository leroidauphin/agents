# coding=utf-8
# Copyright 2018 The TF-Agents Authors.
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

"""Test for tf_agents.environments.suite_gym."""

import functools

import gin

from tf_agents.environments import py_environment
from tf_agents.environments import suite_gym
from tf_agents.environments import wrappers
from tf_agents.utils import test_utils


class SuiteGymTest(test_utils.TestCase):

  def tearDown(self):
    gin.clear_config()
    super(SuiteGymTest, self).tearDown()

  def test_load_adds_time_limit_steps(self):
    env = suite_gym.load('CartPole-v1')
    self.assertIsInstance(env, py_environment.PyEnvironment)
    self.assertIsInstance(env, wrappers.TimeLimit)

  def test_load_disable_step_limit(self):
    env = suite_gym.load('CartPole-v1', max_episode_steps=0)
    self.assertIsInstance(env, py_environment.PyEnvironment)
    self.assertNotIsInstance(env, wrappers.TimeLimit)

  def test_load_disable_wrappers_applied(self):
    duration_wrapper = functools.partial(wrappers.TimeLimit, duration=10)
    env = suite_gym.load(
        'CartPole-v1', max_episode_steps=0, env_wrappers=(duration_wrapper,))
    self.assertIsInstance(env, py_environment.PyEnvironment)
    self.assertIsInstance(env, wrappers.TimeLimit)

  def test_custom_max_steps(self):
    env = suite_gym.load('CartPole-v1', max_episode_steps=5)
    self.assertIsInstance(env, py_environment.PyEnvironment)
    self.assertIsInstance(env, wrappers.TimeLimit)
    self.assertEqual(5, env._duration)

  def testGinConfig(self):
    gin.parse_config_file(
        test_utils.test_src_dir_path('environments/configs/suite_gym.gin')
    )
    env = suite_gym.load()
    self.assertIsInstance(env, py_environment.PyEnvironment)
    self.assertIsInstance(env, wrappers.TimeLimit)

  def test_gym_kwargs_argument(self):
    env = suite_gym.load('FrozenLake-v0', gym_kwargs={'map_name': '4x4'})
    self.assertTupleEqual(env.unwrapped.desc.shape, (4, 4))

    env = suite_gym.load('FrozenLake-v0', gym_kwargs={'map_name': '8x8'})
    self.assertTupleEqual(env.unwrapped.desc.shape, (8, 8))

if __name__ == '__main__':
  test_utils.main()
