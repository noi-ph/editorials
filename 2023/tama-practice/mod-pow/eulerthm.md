% Euler&rsquo;s Theorem


# Euler&rsquo;s Theorem

<div class="editorial-section">
This page contains a proof of [**Euler's theorem**](https://en.wikipedia.org/wiki/Euler%27s_theorem):[^1]



<div class="theorem">
**Euler’s Theorem**. Let $a$ and $m$ be
coprime integers. Then,
$$a^{\varphi(m)} \equiv 1 \pmod m$$
where $\varphi$ is
Euler’s Totient function, and $\varphi(m)$ counts the number of non-negative integers less than $m$ which are coprime to it.
</div>
There are many proofs of Euler’s Theorem online which you can refer to. Here's a classic one:

<details class="proof"><summary class="h4">Proof 1</summary>
Let 
$$S := \{a_1, a_2, \ldots, a_{\varphi(m)}\}$$
be all the non-negative integers $< m$ coprime to $m$. Then I claim 
that
$$\{a\cdot a_1, a\cdot a_2, \ldots, a\cdot a_{\varphi(m)}\}$$
is the same set modulo $m$.

More precisely, we'll show that the map $f: S \to S$ defined as $f: v \mapsto a \cdot v \bmod m$ is well-defined, and is a bijection.

To see this, first note that $a$ is coprime to $m$, so if $v$ is coprime to $m$, then $f(v) = a\cdot v \bmod m$ is also coprime to $m$.
So the map $f$ is well-defined.

Next, we'll show that $f$ is injective.
Suppose $f(a_i) = f(a_j)$; we want to show that $a_i = a_j$. Note that $f(a_i) = f(a_j)$ means that
$a\cdot a_i$ is the same as $a\cdot a_j$ modulo $m$, which by definition means that $m$ divides
$a\cdot a_i - a\cdot a_j = a\cdot (a_i - a_j).$
Now, $m$ and $a$ are coprime, so $m$ divides $a_i - a_j$. Also, $0 \le a_i, a_j < m$, so
$-m < a_i - a_j < m,$
so the only way for $m$ to divide $a_i - a_j$ is if it's zero, so $a_i - a_j = 0$, and $a_i = a_j$.
Therefore, $f$ is injective, and since it's a map from a finite set to a finite set, it's
also surjective, so it's a bijection as claimed.

Since both sets are the same modulo $m$, multiplying all the numbers should give us the same result modulo $m$, i.e.,
$$\begin{align*}
a_1\cdot a_2 \cdots a_{\varphi(m)} &\equiv (a\cdot a_1)\cdot(a\cdot a_2)\cdots (a\cdot a_{\varphi(m)}) \pmod m \\
a_1\cdot a_2 \cdots a_{\varphi(m)} &\equiv a^{\varphi(m)} a_1\cdot a_2\cdots a_{\varphi(m)} \pmod m 
\end{align*}$$
and $m$ divides $a_1\cdot a_2 \cdots a_{\varphi(m)}\cdot (a^{\varphi(m)} - 1)$. But $m$ is coprime with
$a_1\cdot a_2 \cdots a_{\varphi(m)},$
so $m$ must divide $a^{\varphi(m)} - 1$, which is (equivalent to) what we want to prove.
</details> 

Here's another one:

<details class="proof"><summary class="h4">Proof 2</summary>
First, we show that any number $a$ coprime to $m$ has a multiplicative inverse. Using [Bézout's](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity), there exist integers $x$ and $y$ such that
$$ax + my = 1.$$
Reducing this modulo $m$ gives $ax \equiv 1 \pmod{m}$, so $x$ is a multiplicative inverse of $a$.

Next, we show that $a^k \equiv 1 \pmod{m}$ for some positive integer $k$. Consider the sequence $$(1, a, a^2, a^3, \ldots).$$ Considering this sequence *modulo $m$*, each element is between $0$ and $m-1$, so by the pigeonhole principle, they cannot all be distinct modulo $m$; i.e., there exist $0 \le i < j$ such that
$$a^i \equiv a^j \pmod m.$$
Letting $a^{-1}$ be a multiplicative inverse of $a$, multiply both sides by $(a^{-1})^i$ to get
$$1 \equiv a^{j-i} \pmod m,$$
which shows what we want.

Now, let $k$ be the *smallest* positive integer such that $a^k \equiv 1 \pmod{m}$. Let
$$S := \{a_1, a_2, \ldots, a_{\varphi(m)}\}$$
be the set of all the non-negative integers $< m$ coprime to $m$, and consider the equivalence relation $\sim$ on $S$ given by
$$u \sim v \leftrightarrow \text{$u \equiv va^j \!\pmod{m}$ for some $j$}.$$
We can check that this is indeed an equivalence relation:

- $u \equiv ua^0$ so $\sim$ is reflexive;
- $u \equiv va^j$ implies $v \equiv ua^{-j}$, so $\sim$ is symmetric;
- $u \equiv va^i$ and $v \equiv wa^j$ implies $u \equiv wa^{i+j}$, so $\sim$ is transitive.

Thus, we can partition $S$ using this equivalence relation $\sim$. Note that every equivalence class contains exactly $k$ elements, because for every $v \in S$, the following numbers (mod $m$) are all the elements equivalent to $v$ via $\sim$:
$$\{v, va, va^2, \ldots, va^{k-1} \}.$$
Note that further powers of $a$ don't yield new elements because $a^k \equiv 1 \pmod{m}$, and these are all distinct because if $va^i \equiv va^j \pmod{m}$ for $0 \le i < j < k$, then multiplying by the inverses of $v$ and $a^i$ (which are coprime to $m$) yields $a^{j-i} \equiv 1 \pmod{m}$ with $j - i < k$, contradicting the fact that $k$ is the smallest one such that $a^k \equiv 1 \pmod{m}$.

Therefore, all the $\phi(m)$ elements of $S$ are partitioned into equivalence classes, each of which is of size $k$. So if there are $c$ equivalence classes, we have the equation
$$\phi(m) = kc$$
(i.e., $k$ divides $\phi(m)$), and therefore we have
$$a^{\phi(m)} = a^{kc} = (a^k)^c \equiv 1^c = 1 \pmod{m}.$$
</details>

</div>

[^1]: also known as the **Fermat-Euler theorem** because Fermat proved a
    special case (with $m$ prime), and also because Euler already has so
    many things named after him.
