
import numpy as np
import torch
import torch.autograd as autograd

import speech.model

def test_model():
    time_steps = 200
    freq_dim = 120
    output_dim = 10
    batch_size = 4
    seq_len = 20

    config = {
        "encoder_layers" : 1,
        "rnn_dim" : 16
    }

    np.random.seed(1337)
    torch.manual_seed(1337)

    model = speech.model.Model(freq_dim, output_dim, config)

    x = autograd.Variable(torch.randn(batch_size, time_steps, freq_dim))
    labels = np.random.randint(0, output_dim, (batch_size, seq_len))
    y = autograd.Variable(torch.LongTensor(labels))
    output = model.forward(x, y)

    x_enc = model.encode(x)
    out, _, _ = model.decode(x_enc, y)

    hx = None
    out_s = []
    for t in range(seq_len - 1):
        ox, hx = model.decode_step(x_enc, y[:,t], hx=hx)
        out_s.append(ox)
    out_s = torch.stack(out_s, dim=1)
    assert out.size() == out_s.size()
    assert np.allclose(out_s.data.numpy(),
                       out.data.numpy(),
                       rtol=1e-5,
                       atol=1e-7)

