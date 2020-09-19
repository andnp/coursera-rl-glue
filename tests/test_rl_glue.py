import unittest
import numpy as np
from RLGlue import RLGlue, BaseEnvironment, BaseAgent

class MarkovChain(BaseEnvironment):
    def __init__(self):
        self.state = 0
        self.size = 0

    def env_init(self, env_info):
        self.state = env_info['size'] // 2
        self.size = env_info['size']

    def env_start(self):
        return self.state

    def env_step(self, a):
        self.state = self.state + a

        if self.state < 0:
            self.state = 0
        elif self.state >= self.size:
            self.state = self.size - 1

        r = 1 if self.state == 0 else 0
        done = self.state == 0

        return (r, self.state, done)

    def env_cleanup(self):
        pass

    def env_message(self, message):
        pass

class TestAgent(BaseAgent):
    def agent_start(self, s):
        return np.random.choice([-1, 0, 1])

    def agent_step(self, r, s):
        if r is None:
            raise Exception('Expected a reward')
        if s is None:
            raise Exception('Expected a state')

        self.last_reward = r
        self.last_observation = s

        return np.random.choice([-1, 0, 1])

    def agent_end(self, r):
        if r is None:
            raise Exception('Expected a reward')

class TestInterface(unittest.TestCase):
    def test_start(self):
        exp = RLGlue(MarkovChain, TestAgent)

        exp.rl_init(agent_init_info={}, env_init_info={ 'size': 5 })
        state, action = exp.rl_start()

        self.assertEqual(state, 2)
        self.assertIn(action, [-1, 0, 1])

    def test_step(self):
        exp = RLGlue(MarkovChain, TestAgent)

        exp.rl_init(agent_init_info={}, env_init_info={ 'size': 5 })
        exp.rl_start()

        (r, s, a, t) = exp.rl_step()

        self.assertIn(r, [0, 1])
        self.assertIn(s, range(5))
        self.assertIn(a, [-1, 0, 1])
        self.assertIn(t, [True, False])

    def test_episode(self):
        np.random.seed(0)
        exp = RLGlue(MarkovChain, TestAgent)

        exp.rl_init(agent_init_info={}, env_init_info={ 'size': 5 })
        exp.rl_start()

        terminated = exp.rl_episode(100)

        self.assertIn(terminated, [True, False])
        self.assertIn(exp.num_steps, range(100))
        self.assertEqual(exp.total_reward, 1)
        self.assertEqual(exp.num_episodes, 1)

        # test other parts of the api
        self.assertIn(exp.rl_num_steps(), range(100))
        self.assertEqual(exp.rl_return(), 1)
        self.assertEqual(exp.rl_num_episodes(), 1)

    def test_episodes(self):
        np.random.seed(0)
        exp = RLGlue(MarkovChain, TestAgent)

        exp.rl_init(agent_init_info={}, env_init_info={ 'size': 5 })
        exp.rl_start()

        # simulate 100 episodes
        for _ in range(100):
            terminated = exp.rl_episode(1000)

            self.assertIn(terminated, [True, False])

        # test other parts of the api
        self.assertIn(exp.rl_num_steps(), range(100 * 1000))
        self.assertEqual(exp.rl_return(), 100)
        self.assertEqual(exp.rl_num_episodes(), 100)
