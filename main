const express = require('express');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static('public'));

// 임시 데이터
let kits = [
  { id: 1, title: 'EXERCISE 운동 키트 (라텍스밴드+지압판+폴리모프)', price: 15000, desc: '나만의 운동 기구를 만드는 DIY 키트입니다.' }
];

let userProducts = [
  { id: 1, title: '폴리모프 커스텀 지압 악력기', seller: '정예나', price: 12000, desc: '키트로 제작한 맞춤형 악력기입니다.' }
];

// API 라우트
app.get('/api/kits', (req, res) => {
  res.json(kits);
});

app.get('/api/user-products', (req, res) => {
  res.json(userProducts);
});

app.post('/api/user-products', (req, res) => {
  const { title, seller, price, desc } = req.body;
  const newProduct = {
    id: userProducts.length + 1,
    title: title,
    seller: seller,
    price: Number(price),
    desc: desc
  };
  userProducts.push(newProduct);
  res.status(201).json({ message: '물품이 성공적으로 등록되었습니다.', product: newProduct });
});

app.listen(PORT, () => {
  console.log('Server running at http://localhost:' + PORT);
});
