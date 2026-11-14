# Geometry for scan simulation

To simulate a scan, we represent the laser beam as a **ray** and the alcove walls as **planes**. Calculating where they intersect lets us predict where the laser would hit and what distance it would measure.

This is useful for testing scanner positions and estimating coverage without needing the physical scanner.

## Dot product

The dot product multiplies the corresponding components of two vectors and adds the results, producing a scalar (a single number).

For example:

$$
\begin{aligned}
\mathbf a\cdot\mathbf b
&=(2,3,4)\cdot(5,1,2)\\
&=(2\times5)+(3\times1)+(4\times2)\\
&=21
\end{aligned}
$$

The dot product also relates to the angle between two vectors:

$$
\boxed{\mathbf a\cdot\mathbf b=|\mathbf a||\mathbf b|\cos\theta}
$$

Here, $\theta$ is the angle between them and $|\mathbf a|$ is the length of vector $\mathbf a$.

When the dot product is zero, the vectors are perpendicular (provided neither is a zero vector).

## Rays and planes

### Ray

A ray starts at a point and extends indefinitely in one direction.

$$
\boxed{\mathbf p(t)=\mathbf p_0+t\mathbf v}
$$

- $\mathbf p_0$ - starting position
- $\mathbf v$ - direction vector
- $t$ - how far to travel along the direction
- $\mathbf p(t)$ - resulting position

For a ray, $t\geq0$. If $\mathbf v$ is a **unit vector** (length 1), $t$ is the physical distance travelled. Otherwise, it's a scaling factor.

### Plane

A plane is an infinitely large flat surface, defined by:

$$
\boxed{\mathbf p\cdot\mathbf n=d}
$$

- $\mathbf p$ - any point on the plane
- $\mathbf n$ - the normal vector, perpendicular to the plane
- $d$ - a constant defining the plane's position

For example, a wall at $y=4$ has normal $\mathbf n=(0,1,0)$.

For any point $\mathbf p=(x,y,z)$:

$$
\mathbf p\cdot\mathbf n=(x,y,z)\cdot(0,1,0)=y
$$

So $\mathbf p\cdot\mathbf n=4$ is simply another way of writing $y=4$.

Using a normal vector also lets us describe walls that aren't aligned with the coordinate axes.

## Ray–plane intersection

We want to find the value of $t$ at which the ray intersects the plane.

Starting with the two equations:

$$
\mathbf p(t)=\mathbf p_0+t\mathbf v
$$

$$
\mathbf p\cdot\mathbf n=d
$$

Substitute the ray into the plane equation:

$$
(\mathbf p_0+t\mathbf v)\cdot\mathbf n=d
$$

Expand the dot product:

$$
\mathbf p_0\cdot\mathbf n+t(\mathbf v\cdot\mathbf n)=d
$$

Rearrange for $t$:

$$
\boxed{t=\frac{d-\mathbf p_0\cdot\mathbf n}{\mathbf v\cdot\mathbf n}}
$$

We can then substitute $t$ back into the ray equation to find the intersection coordinates.

### Example

Suppose we have a ray starting at $(1,1,1)$, travelling in direction $(2,1,0)$, and a wall at $y=4$.

$$
\begin{aligned}
\mathbf p_0&=(1,1,1)\\
\mathbf v&=(2,1,0)\\
\mathbf n&=(0,1,0)\\
d&=4
\end{aligned}
$$

Calculate the intersection parameter:

$$
t=\frac{4-1}{1}=3
$$

Substitute into the ray equation:

$$
\begin{aligned}
\mathbf p(3)&=(1,1,1)+3(2,1,0)\\
&=\boxed{(7,4,1)}
\end{aligned}
$$

The resulting Y coordinate is 4, so the point lies on the wall.

**Note:** Since the direction isn't normalised, $t=3$ isn't the laser's distance measurement. The actual distance is:

$$
\sqrt{6^2+3^2}=\sqrt{45}\approx6.71
$$

If the coordinates are in millimetres, the distance is also in millimetres. Our Python implementation normalises the direction before calculating the intersection.

## Edge cases

- **Parallel rays:** If $\mathbf v\cdot\mathbf n=0$, there is no unique intersection. The ray either misses the plane or lies within it.
- **Intersection behind the scanner:** If $t<0$, the intersection is behind the ray's origin and should be ignored.
- **Nearly parallel rays:** Small angular changes can cause large changes in the intersection position. This matters when the laser hits a wall at a grazing angle.
- **Wall boundaries:** Planes are infinite, but real walls aren't. We need to check that an intersection falls within the wall's actual dimensions.

## Reference

[3D Math Primer for Graphics and Game Development - Geometric Tests](https://www.gamemath.com/book/geomtests.html), section A.9, _Intersection of a Ray and Plane_.
