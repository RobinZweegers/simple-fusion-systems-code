import numpy as np

# helper for NT ; reduces to the orginal elongation funtion as used in the preivous systems code
def _miller_boundary(r_major, r_minor, kappa, delta, npts=2048):
    theta = np.linspace(0.0, 2.0*np.pi, npts, endpoint=False)
    delta = float(np.clip(delta, -0.8, 0.8))
    alpha = np.arcsin(delta)

    r = r_major + r_minor * np.cos(theta + alpha * np.sin(theta))
    z = kappa * r_minor * np.sin(theta)

    return r, z


def _closed_curve_area(r, z):
    r_next = np.roll(r, -1)
    z_next = np.roll(z, -1)
    return 0.5 * np.abs(np.sum(r * z_next - r_next * z))

def _surface_of_revolution(r, z):
    r_next = np.roll(r, -1)
    z_next = np.roll(z, -1)
    ds = np.sqrt((r_next - r)**2 + (z_next - z)**2)
    r_mid = 0.5 * (r + r_next)
    return 2.0 * np.pi * np.sum(r_mid * ds)

def _boundary_perimeter(r, z):
    r_next = np.roll(r, -1)
    z_next = np.roll(z, -1)

    ds = np.sqrt((r_next - r)**2 + (z_next - z)**2)

    return np.sum(ds)

# uses the previous two helpers and returns the entire plasma / shape geometry
def shape_geometry(r_major, r_minor, kappa, delta):
    r, z = _miller_boundary(r_major, r_minor, kappa, delta)
    area = _closed_curve_area(r, z)
    surface = _surface_of_revolution(r, z)
    volume = 2.0 * np.pi * r_major * area
    perimeter = _boundary_perimeter(r,z)
    return area, perimeter, surface, volume



def ip_shape_factor(delta, c1=0.15, c2=0.10):
    """
        needed for taking triangularity into account => simple fit; kinda need sum papers for this tbh
    """
    return 1.0 + c1*delta + c2*delta**2

def sauter_ip_shape_factor(kappa: float, delta: float, squareness: float = 1.0) -> float:
	"""
	Engineering fit for shaping effect on plasma current / q95 based on Sauter et al.
	The w07 squareness factor is held at 1.0 because this simple model does not resolve squareness.
     
     taken from : https://pdf.sciencedirectassets.com/271368/1-s2.0-S0920379616X00099/1-s2.0-S0920379616303234/main.pdf
     """
	kappa_term = 1.0 + 1.2 * (kappa - 1.0) + 0.56 * (kappa - 1.0)**2
	delta_term = (1.0 + 0.09 * delta + 0.16 * delta**2) / (1.0 + 0.45 * delta)
	shape_term = 1.0 - 0.74 * delta * squareness
	square_term = 1.0 + 0.55 * (squareness - 1.0)
	return kappa_term * delta_term / shape_term * square_term